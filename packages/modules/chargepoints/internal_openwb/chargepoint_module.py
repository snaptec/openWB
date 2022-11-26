import logging
import RPi.GPIO as GPIO
import time
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

from modules.common.abstract_chargepoint import AbstractChargepoint
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import ChargepointState
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.modbus import ModbusSerialClient_
from modules.common.store import ramdisk_read, ramdisk_write
from modules.common import sdm
from modules.common import evse
from modules.common import b32
from modules.common.store import get_chargepoint_value_store

log = logging.getLogger(__name__)


def get_default_config() -> Dict:
    return {"id": 0,
            "serial_client": None,  # type: Optional[ModbusSerialClient_]
            "connection_module": {
                "client": None  # type: Optional[CONNECTION_MODULES]
            },
            "power_module": {
                "client": None  # type: Optional[evse.Evse]
            }}


CONNECTION_MODULES = Union[sdm.Sdm630, b32.B32]


class InternalOpenWB:
    def __init__(self, id: int, serial_client: ModbusSerialClient_) -> None:
        self.id = id
        self.serial_client = serial_client


class ClientFactory:
    def __init__(self, local_charge_point_num: int, serial_client: ModbusSerialClient_) -> None:
        self.local_charge_point_num = local_charge_point_num
        self.meter_client, self.evse_client = self.__factory(serial_client)
        self.read_error = 0

    def __factory(self, serial_client: ModbusSerialClient_) -> Tuple[CONNECTION_MODULES, evse.Evse]:
        meter_config = NamedTuple("MeterConfig", [('type', CONNECTION_MODULES), ('modbus_id', int)])
        meter_configuration_options = [
            [meter_config(sdm.Sdm630, modbus_id=105), meter_config(b32.B32, modbus_id=201)],
            [meter_config(sdm.Sdm630, modbus_id=106)]
        ]

        def _check_meter(serial_client: ModbusSerialClient_, meters: List[meter_config]):
            for meter_type, modbus_id in meters:
                try:
                    meter_client = meter_type(modbus_id, serial_client)
                    if meter_client.get_voltages()[0] > 20:
                        return meter_client
                except Exception:
                    pass
            else:
                raise Exception("Es konnte keines der Meter in "+str(meters)+" zugeordnet werden.")

        meter_client = _check_meter(serial_client, meter_configuration_options[self.local_charge_point_num - 1])
        evse_client = evse.Evse(self.local_charge_point_num, serial_client)
        return meter_client, evse_client

    def get_pins_phase_switch(self, new_phases: int) -> Tuple[int, int]:
        # return gpio_cp, gpio_relay
        if self.local_charge_point_num == 1:
            return 22, 29 if new_phases == 1 else 37
        else:
            return 15, 11 if new_phases == 1 else 13

    def get_pins_cp_interruption(self) -> int:
        # return gpio_cp, gpio_relay
        if self.local_charge_point_num == 1:
            return 22
        else:
            return 15


class ChargepointModule(AbstractChargepoint):
    PLUG_STANDBY_POWER_THRESHOLD = 10

    def __init__(self, config: InternalOpenWB) -> None:
        self.config = config
        self.component_info = ComponentInfo(
            self.config.id,
            "Ladepunkt "+str(self.config.id), "chargepoint")
        self.__store = get_chargepoint_value_store(self.config.id)
        self.__client = ClientFactory(self.config.id, self.config.serial_client)
        self.old_plug_state = False

    def set_current(self, current: float) -> None:
        with SingleComponentUpdateContext(self.component_info):
            if self.set_current_evse != current:
                self.__client.evse_client.set_current(int(current))

    def get_values(self, phase_switch_cp_active: bool) -> Tuple[ChargepointState, float]:
        try:
            _, power = self.__client.meter_client.get_power()
            if power < self.PLUG_STANDBY_POWER_THRESHOLD:
                power = 0
            voltages = self.__client.meter_client.get_voltages()
            currents = self.__client.meter_client.get_currents()
            imported = self.__client.meter_client.get_imported()
            phases_in_use = sum(1 for current in currents if current > 3)

            time.sleep(0.1)
            plug_state, charge_state, self.set_current_evse = self.__client.evse_client.get_plug_charge_state()
            self.__client.read_error = 0

            rfid = ramdisk_read("readtag")
            # reset tag
            if rfid != "0" and plug_state is False:
                ramdisk_write("readtag", "0")

            if phase_switch_cp_active:
                # Während des Threads wird die CP-Leitung unterbrochen, das EV soll aber als angesteckt betrachtet
                # werden. In 1.9 war das kein Problem, da währendessen keine Werte von der EVSE abgefragt wurden.
                log.debug(
                    "Plug_state %s beibehalten, da CP-Unterbrechung oder Phasenumschaltung aktiv.", self.old_plug_state
                )
                plug_state = self.old_plug_state
            else:
                self.old_plug_state = plug_state

            if (max(currents) > 0.1 and charge_state is False) or (max(currents) == 0 and charge_state):
                raise ValueError("Ladestatus {} passt nicht zu den Strömen {}.".format(charge_state, currents))

            chargepoint_state = ChargepointState(
                power=power,
                currents=currents,
                imported=imported,
                exported=0,
                # powers=powers,
                voltages=voltages,
                # frequency=frequency,
                plug_state=plug_state,
                charge_state=charge_state,
                phases_in_use=phases_in_use,
                rfid=rfid
            )
        except Exception as e:
            self.__client.read_error += 1
            if self.__client.read_error > 5:
                log.exception(
                    "Anhaltender Fehler beim Auslesen der EVSE. Lade- und Steckerstatus werden zurückgesetzt.")
                plug_state = False
                charge_state = False
                chargepoint_state = ChargepointState(
                    plug_state=plug_state,
                    charge_state=charge_state,
                    phases_in_use=0
                )
                FaultState.error(__name__ + " " + str(type(e)) + " " + str(e)).store_error(self.component_info)
            else:
                raise FaultState.error(__name__ + " " + str(type(e)) + " " + str(e)) from e

        self.__store.set(chargepoint_state)
        return chargepoint_state, self.set_current_evse

    def perform_phase_switch(self, phases_to_use: int, duration: int) -> None:
        gpio_cp, gpio_relay = self.__client.get_pins_phase_switch(phases_to_use)
        with SingleComponentUpdateContext(self.component_info):
            self.__client.evse_client.set_current(0)
        time.sleep(1)
        GPIO.output(gpio_cp, GPIO.HIGH)  # CP off
        GPIO.output(gpio_relay, GPIO.HIGH)  # 3 on/off
        time.sleep(duration)
        GPIO.output(gpio_relay, GPIO.LOW)  # 3 on/off
        time.sleep(duration)
        GPIO.output(gpio_cp, GPIO.LOW)  # CP on
        time.sleep(1)

    def perform_cp_interruption(self, duration: int) -> None:
        gpio_cp = self.__client.get_pins_cp_interruption()
        with SingleComponentUpdateContext(self.component_info):
            self.__client.evse_client.set_current(0)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gpio_cp, GPIO.OUT)

        GPIO.output(gpio_cp, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(gpio_cp, GPIO.LOW)
