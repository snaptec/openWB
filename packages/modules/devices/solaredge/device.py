#!/usr/bin/env python3
import logging
from operator import add
from statistics import mean
import time
from typing import Dict, Iterable, Tuple, Union, Optional, List
from urllib3.util import parse_url

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import BatState, InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store, get_bat_value_store
from modules.devices.solaredge import bat, counter, external_inverter, inverter
from modules.devices.solaredge.bat import SolaredgeBat
from modules.devices.solaredge.counter import SolaredgeCounter
from modules.devices.solaredge.external_inverter import SolaredgeExternalInverter
from modules.devices.solaredge.inverter import SolaredgeInverter
from modules.devices.solaredge.config import (Solaredge, SolaredgeBatConfiguration, SolaredgeBatSetup,
                                              SolaredgeConfiguration,
                                              SolaredgeCounterConfiguration, SolaredgeCounterSetup,
                                              SolaredgeExternalInverterConfiguration, SolaredgeExternalInverterSetup,
                                              SolaredgeInverterConfiguration, SolaredgeInverterSetup)
from modules.devices.solaredge.meter import SolaredgeMeterRegisters

log = logging.getLogger(__name__)

solaredge_component_classes = Union[SolaredgeBat, SolaredgeCounter,
                                    SolaredgeExternalInverter, SolaredgeInverter]
default_unit_id = 85
synergy_unit_identifier = 160
reconnect_delay = 1.2


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": SolaredgeBat,
        "counter": SolaredgeCounter,
        "inverter": SolaredgeInverter,
        "external_inverter": SolaredgeExternalInverter
    }

    def __init__(self, device_config: Union[Dict, Solaredge]) -> None:
        self.components = {}  # type: Dict[str, solaredge_component_classes]
        try:
            self.device_config = dataclass_from_dict(Solaredge, device_config)
            self.client = modbus.ModbusTcpClient_(self.device_config.configuration.ip_address,
                                                  self.device_config.configuration.port)
            self.inverter_counter = 0
            self.synergy_units = 1
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self,
                      component_config:  Union[dict,
                                               SolaredgeBatSetup,
                                               SolaredgeCounterSetup,
                                               SolaredgeExternalInverterSetup,
                                               SolaredgeInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config, self.client))
            if component_type == "inverter" or component_type == "external_inverter":
                self.inverter_counter += 1
            # try:
            #     # ToDo: convert to String
            #     manufacturer = self.client.read_holding_registers(40004, [modbus.ModbusDataType.UINT_32]*8,
            #                                                       unit=component_config.configuration.modbus_id)
            #     # ToDo: convert to String
            #     model = self.client.read_holding_registers(40020, [modbus.ModbusDataType.UINT_32]*8,
            #                                                unit=component_config.configuration.modbus_id)
            #     # ToDo: convert to String
            #     version = self.client.read_holding_registers(40044, [modbus.ModbusDataType.UINT_16]*8,
            #                                                  unit=component_config.configuration.modbus_id)
            #     serial_number = self.client.read_holding_registers(40052, [modbus.ModbusDataType.UINT_32]*8,
            #                                                        unit=component_config.configuration.modbus_id)
            #     log.debug("Version: " + str(version))
            # except Exception as e:
            #     log.exception("Fehler beim Auslesen der Modbus-Register: " + str(e))
            #     pass
            if self.client.read_holding_registers(40121, modbus.ModbusDataType.UINT_16,
                                                  unit=component_config.configuration.modbus_id
                                                  ) == synergy_unit_identifier:
                log.debug("Synergy Units supported")
                self.synergy_units = int(self.client.read_holding_registers(
                    40129, modbus.ModbusDataType.UINT_16,
                    unit=component_config.configuration.modbus_id)) or 1
                log.debug("Synergy Units detected: %s", self.synergy_units)
            if component_type == "external_inverter" or component_type == "counter" or component_type == "inverter":
                self.set_component_registers(self.components.values(), self.synergy_units)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    @staticmethod
    def set_component_registers(components: Iterable[solaredge_component_classes], synergy_units: int) -> None:
        meters = [None]*3  # type: List[Union[SolaredgeExternalInverter, SolaredgeCounter, None]]
        for component in components:
            if isinstance(component, (SolaredgeExternalInverter, SolaredgeCounter)):
                meters[component.component_config.configuration.meter_id-1] = component

        # https://www.solaredge.com/sites/default/files/sunspec-implementation-technical-note.pdf:
        # Only enabled meters are readable, i.e. if meter 1 and 3 are enabled, they are readable as 1st meter and 2nd
        # meter (and the 3rd meter isn't readable).
        for meter_id, meter in enumerate(filter(None, meters), start=1):
            log.debug(
                "%s: internal meter id: %d, synergy units: %s", meter.component_config.name, meter_id, synergy_units
            )
            meter.registers = SolaredgeMeterRegisters(meter_id, synergy_units)

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            with self.client:
                for component in self.components:
                    # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                    with SingleComponentUpdateContext(self.components[component].component_info):
                        self.components[component].update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "external_inverter": external_inverter,
    "inverter": inverter
}


def read_legacy(component_type: str,
                ip_address: str,
                port: str,
                slave_id0: str,
                slave_id1: Optional[str] = None,
                slave_id2: Optional[str] = None,
                slave_id3: Optional[str] = None,
                batwrsame: Optional[int] = None,
                extprodakt: Optional[int] = None,
                zweiterspeicher: Optional[int] = None,
                subbat: Optional[int] = None,
                ip2address: Optional[str] = None,
                num: Optional[int] = None) -> None:
    def get_bat_state() -> Tuple[List, BatState]:
        def create_bat(modbus_id: int) -> bat.SolaredgeBat:
            component_config = SolaredgeBatSetup(id=num,
                                                 configuration=SolaredgeBatConfiguration(modbus_id=modbus_id))
            return bat.SolaredgeBat(dev.device_config.id, component_config, dev.client)
        bats = [create_bat(int(slave_id0))]
        if zweiterspeicher == 1:
            bats.append(create_bat(int(slave_id1)))
        soc_bat, power_bat = [], []
        for battery in bats:
            power, soc = battery.get_values()
            power_bat.append(power)
            soc_bat.append(soc)
        imported, exported = bats[0].get_imported_exported(sum(power_bat))
        return power_bat, BatState(power=sum(power_bat), soc=mean(soc_bat), imported=imported, exported=exported)

    def get_external_inverter_state(dev: Device, id: int) -> InverterState:
        component_config = SolaredgeExternalInverterSetup(id=num,
                                                          configuration=SolaredgeExternalInverterConfiguration(
                                                              modbus_id=id))

        ext_inverter = SolaredgeExternalInverter(
            dev.device_config.id, component_config, dev.client)
        return ext_inverter.read_state()

    def create_inverter(modbus_id: int) -> SolaredgeInverter:
        component_config = SolaredgeInverterSetup(id=num,
                                                  configuration=SolaredgeInverterConfiguration(modbus_id=modbus_id))
        return SolaredgeInverter(dev.device_config.id, component_config, dev.client)

    log.debug("Solaredge IP: "+ip_address+":"+str(port))
    log.debug("Solaredge Slave-IDs: ["+str(slave_id0)+", "+str(slave_id1)+", "+str(slave_id2)+", "+str(slave_id3)+"]")
    log.debug("Solaredge Bat-WR-gleiche IP: "+str(batwrsame)+", Externer WR: "+str(extprodakt) +
              ", 2. Speicher: "+str(zweiterspeicher)+", Speicherleistung subtrahieren: "+str(subbat)+" 2. IP: " +
              str(ip2address)+", Num: "+str(num))

    if port == "":
        parsed_url = parse_url(ip_address)
        ip_address = parsed_url.hostname
        if parsed_url.port:
            port = parsed_url.port
        else:
            port = 502
    dev = Device(Solaredge(configuration=SolaredgeConfiguration(ip_address=ip_address, port=int(port))))
    if component_type == "counter":
        dev.add_component(SolaredgeCounterSetup(
            id=num, configuration=SolaredgeCounterConfiguration(modbus_id=int(slave_id0))))
        log.debug('Solaredge ModbusID: ' + str(slave_id0))
        dev.update()
    elif component_type == "inverter":
        if ip2address == "none":
            modbus_ids = list(map(int,
                                  filter(lambda id: id.isnumeric(),
                                         [slave_id0, slave_id1, slave_id2, slave_id3])))
            inverters = [create_inverter(modbus_id) for modbus_id in modbus_ids]
            with SingleComponentUpdateContext(inverters[0].component_info):
                total_power = 0
                total_energy = 0
                total_currents = [0.0]*3
                with dev.client:
                    for inv in inverters:
                        state = inv.read_state()
                        if state.dc_power == 0:
                            total_power += 0
                        else:
                            total_power += state.power
                        total_energy += state.exported
                        total_currents = list(map(add, total_currents, state.currents))

                    if extprodakt:
                        external_inv_power = get_external_inverter_state(dev, int(slave_id0)).power
                        total_power += external_inv_power
                    else:
                        external_inv_power = 0

                    if batwrsame == 1:
                        bat_power, bat_state = get_bat_state()
                        # WR-Leistung nur anpassen, wenn die Ladeleistung des Speichers PV-Leistung ist, dh am WR muss
                        # DC-seitig Leistung anliegen. Der Speicher wird auch aus dem Netz geladen, um einen
                        # Mindest-SoC zu halten.
                        # Wenn ein weiterer WR über ein Smartmeter angeschlossen ist, kann der Speicher auch über
                        # diesen geladen werden.
                        if state.dc_power is None or state.dc_power <= 0 or external_inv_power < 0:
                            if subbat == 1:
                                total_power -= sum(min(p, 0) for p in bat_power)
                            else:
                                total_power -= sum(bat_power)
                        total_energy = total_energy + bat_state.imported - bat_state.exported
                if batwrsame == 1:
                    get_bat_value_store(1).set(bat_state)
                get_inverter_value_store(num).set(InverterState(exported=total_energy,
                                                                power=min(0, total_power), currents=total_currents))
        else:
            inv = create_inverter(int(slave_id0))
            with SingleComponentUpdateContext(inv.component_info):
                with dev.client:
                    state = inv.read_state()
                    total_power = state.power
                    total_energy = state.exported

                    if batwrsame == 1:
                        zweiterspeicher = 0
                        bat_power, bat_state = get_bat_state()
                        if state.dc_power is None or state.dc_power <= 0:
                            total_power -= sum(bat_power)
                        total_energy = total_energy + bat_state.imported - bat_state.exported
                        get_bat_value_store(1).set(bat_state)
                device_config = Solaredge(configuration=SolaredgeConfiguration(ip_address=ip2address))
                dev = Device(device_config)
                inv = create_inverter(int(slave_id0))
                with dev.client:
                    state = inv.read_state()
                    total_power += state.power
                    total_energy += state.exported
                    if extprodakt:
                        state = get_external_inverter_state(dev, int(slave_id0))
                        total_power += state.power
                get_inverter_value_store(num).set(InverterState(exported=total_energy, power=total_power))
        time.sleep(reconnect_delay)

    elif component_type == "bat":
        with SingleComponentUpdateContext(ComponentInfo(0, "Solaredge Speicher", "bat")):
            get_bat_value_store(1).set(get_bat_state()[1])


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Solaredge)
