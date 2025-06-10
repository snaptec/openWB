import logging
import RPi.GPIO as GPIO
import time
from typing import Tuple

from modules.common.abstract_chargepoint import AbstractChargepoint
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import ChargepointState
from modules.common.fault_state import ComponentInfo, FaultState
from modules.common.store import get_chargepoint_value_store, ramdisk_read
from modules.internal_chargepoint_handler.clients import ClientHandler
log = logging.getLogger(__name__)


class ChargepointModule(AbstractChargepoint):
    PLUG_STANDBY_POWER_THRESHOLD = 10

    def __init__(self, local_charge_point_num: int, client_handler: ClientHandler, parent_hostname: str) -> None:
        self.local_charge_point_num = local_charge_point_num
        self.component_info = ComponentInfo(
            local_charge_point_num,
            "Ladepunkt "+str(local_charge_point_num), "chargepoint", parent_hostname)
        self.store = get_chargepoint_value_store(local_charge_point_num)
        self.old_plug_state = False
        self.__client = client_handler
        time.sleep(0.1)
        self.__client.evse_client.get_firmware_version()
        self.__client.evse_client.deactivate_precise_current()

    def set_current(self, current: float) -> None:
        with SingleComponentUpdateContext(self.component_info):
            if self.set_current_evse != current:
                self.__client.evse_client.set_current(int(current))

    def get_values(self, phase_switch_cp_active: bool) -> Tuple[ChargepointState, float]:
        try:
            powers, power = self.__client.meter_client.get_power()
            if power < self.PLUG_STANDBY_POWER_THRESHOLD:
                power = 0
            voltages = self.__client.meter_client.get_voltages()
            currents = self.__client.meter_client.get_currents()
            imported = self.__client.meter_client.get_imported()
            power_factors = self.__client.meter_client.get_power_factors()
            frequency = self.__client.meter_client.get_frequency()
            phases_in_use = sum(1 for current in currents if current > 3)

            time.sleep(0.1)
            plug_state, charge_state, self.set_current_evse = self.__client.evse_client.get_plug_charge_state()
            self.__client.read_error = 0

            rfid = ramdisk_read("readtag")

            if phase_switch_cp_active:
                # Während des Threads wird die CP-Leitung unterbrochen, das EV soll aber als angesteckt betrachtet
                # werden. In 1.9 war das kein Problem, da währenddessen keine Werte von der EVSE abgefragt wurden.
                log.debug(
                    "Plug_state %s beibehalten, da CP-Unterbrechung oder Phasenumschaltung aktiv.", self.old_plug_state
                )
                plug_state = self.old_plug_state
            else:
                self.old_plug_state = plug_state

            chargepoint_state = ChargepointState(
                power=power,
                currents=currents,
                imported=imported,
                exported=0,
                powers=powers,
                voltages=voltages,
                frequency=frequency,
                plug_state=plug_state,
                charge_state=charge_state,
                phases_in_use=phases_in_use,
                power_factors=power_factors,
                rfid=rfid
            )
        except Exception as e:
            self.__client.read_error += 1
            if self.__client.read_error > 5:
                log.exception(
                    "Anhaltender Fehler beim Auslesen der EVSE. Lade- und Stecker-Status werden zurückgesetzt.")
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

        self.store.set(chargepoint_state)
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
