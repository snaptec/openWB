#!/usr/bin/env python3
import logging
from operator import add
from statistics import mean
from typing import Dict, Tuple, Union, Optional, List
from urllib3.util import parse_url

try:
    from control import data
except ImportError:
    # Modul wird nur in 2.0 benötigt und ist in 1.9 nicht vorhanden
    pass
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext, SingleComponentUpdateContext
from modules.common.component_state import BatState, InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store, get_bat_value_store
from modules.solaredge import bat
from modules.solaredge import counter
from modules.solaredge import external_inverter
from modules.solaredge import inverter


log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "SolarEdge",
        "type": "solaredge",
        "id": 0,
        "configuration": {
            "ip_address": None,
            "port": 502,
            "fix_only_bat_discharging": False
        }
    }


solaredge_component_classes = Union[bat.SolaredgeBat, counter.SolaredgeCounter,
                                    external_inverter.SolaredgeExternalInverter, inverter.SolaredgeInverter]
default_unit_id = 85


class SolaredgeConfiguration:
    def __init__(self, ip_address: str, port: int, fix_only_bat_discharging: bool):
        self.ip_address = ip_address
        self.port = port
        self.fix_only_bat_discharging = fix_only_bat_discharging

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["ip_address", "port", "fix_only_bat_discharging"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return SolaredgeConfiguration(*values)


class Solaredge:
    def __init__(self, name: str, type: str, id: int, configuration: SolaredgeConfiguration) -> None:
        self.name = name
        self.type = type
        self.id = id
        self.configuration = configuration

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["name", "type", "id", "configuration"]
        try:
            values = [device_config[key] for key in keys]
            values = []
            for key in keys:
                if isinstance(device_config[key], Dict):
                    values.append(SolaredgeConfiguration.from_dict(device_config[key]))
                else:
                    values.append(device_config[key])
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return Solaredge(*values)


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.SolaredgeBat,
        "counter": counter.SolaredgeCounter,
        "inverter": inverter.SolaredgeInverter,
        "external_inverter": external_inverter.SolaredgeExternalInverter
    }

    def __init__(self, device_config: Union[dict, Solaredge]) -> None:
        self.components = {}  # type: Dict[str, solaredge_component_classes]
        try:
            self.device_config = device_config \
                if isinstance(device_config, Solaredge) \
                else Solaredge.from_dict(device_config)
            self.client = modbus.ModbusClient(self.device_config.configuration.ip_address,
                                              self.device_config.configuration.port)
            self.inverter_counter = 0
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config, self.client))
            if component_type == "inverter" or component_type == "external_inverter":
                self.inverter_counter += 1
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            total_power = 0
            with MultiComponentUpdateContext(self.components):
                for component in self.components.values():
                    if isinstance(component, bat.SolaredgeBat):
                        parent = data.data.counter_data["all"].get_entry_of_parent(component.component_config["id"])
                        if parent.get("type") != "inverter":
                            log.warning("Solaredge-Speicher sollten als Hybrid-System konfiguriert werden, d.h. die " +
                                        "Speicher sind in der Hierarchie unter den Wechselrichtern anzuordnen.")
                        state = component.read_state()
                        component.update(state)
                        if self.device_config.configuration.fix_only_bat_discharging:
                            total_power -= min(state.power, 0)
                        else:
                            total_power -= state.power
                for component in self.components.values():
                    if (isinstance(component, inverter.SolaredgeInverter) or
                            isinstance(component, external_inverter.SolaredgeExternalInverter)):
                        state = component.read_state()
                        # In 1.9 wurde bisher die Summe der WR-Leistung um die Summe der Batterie-Leistung bereinigt.
                        # Zähler und Ströme wurden nicht bereinigt.
                        state.power = state.power - total_power/self.inverter_counter
                        component.update(state)
                for component in self.components.values():
                    if isinstance(component, counter.SolaredgeCounter):
                        component.update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


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
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }

    def get_bat_state() -> Tuple[List, List]:
        def create_bat(modbus_id: int) -> bat.SolaredgeBat:
            component_config["id"] = num
            component_config["configuration"]["modbus_id"] = modbus_id
            return bat.SolaredgeBat(dev.device_config.id, component_config, dev.client)
        bats = [create_bat(1)]
        if zweiterspeicher == 1:
            bats.append(create_bat(2))
        soc_bat, power_bat = [], []
        for battery in bats:
            state = battery.read_state()
            power_bat.append(state.power)
            soc_bat.append(state.soc)
        return power_bat, soc_bat

    def get_external_inverter_state(dev: Device, id: int) -> InverterState:
        component_config["id"] = num
        component_config["configuration"]["modbus_id"] = id
        ext_inverter = external_inverter.SolaredgeExternalInverter(
            dev.device_config.id, component_config, dev.client)
        return ext_inverter.read_state()

    def create_inverter(modbus_id: int) -> inverter.SolaredgeInverter:
        component_config["id"] = num
        component_config["configuration"]["modbus_id"] = modbus_id
        return inverter.SolaredgeInverter(dev.device_config.id, component_config, dev.client)

    log.debug("Solaredge IP: "+ip_address+":"+str(port))
    log.debug("Solaredge Slave-IDs: ["+str(slave_id0)+", "+str(slave_id1)+", "+str(slave_id2)+", "+str(slave_id3)+"]")
    log.debug("Solaredge Bat-WR-gleiche IP: "+str(batwrsame)+", Externer WR: "+str(extprodakt) +
              ", 2. Speicher: "+str(zweiterspeicher)+", Speicherleistung subtrahieren: "+str(subbat)+" 2. IP: " +
              str(ip2address)+", Num: "+str(num))

    device_config = Solaredge.from_dict(get_default_config())
    if port == "":
        parsed_url = parse_url(ip_address)
        ip_address = parsed_url.hostname
        if parsed_url.port:
            port = parsed_url.port
        else:
            port = 502
    device_config.configuration.ip_address = ip_address
    device_config.configuration.port = int(port)
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    if component_type == "counter":
        component_config["id"] = num
        component_config["configuration"]["modbus_id"] = int(slave_id0)
        dev.add_component(component_config)
        log.debug('Solaredge ModbusID: ' + str(slave_id0))
        dev.update()
    elif component_type == "inverter":
        if ip2address == "none":
            modbus_ids = list(map(int, filter(lambda id: id.isnumeric(), [slave_id0, slave_id1, slave_id2, slave_id3])))
            inverters = [create_inverter(modbus_id) for modbus_id in modbus_ids]
            with SingleComponentUpdateContext(inverters[0].component_info):
                total_power = 0
                total_energy = 0
                total_currents = [0.0]*3
                for inv in inverters:
                    state = inv.read_state()
                    total_power -= state.power
                    total_energy += state.counter
                    total_currents = list(map(add, total_currents, state.currents))

                if extprodakt:
                    state = get_external_inverter_state(dev, int(slave_id0))
                    total_power -= state.power

                if batwrsame == 1:
                    bat_power, soc_bat = get_bat_state()
                    if subbat == 1:
                        total_power -= sum(min(p, 0) for p in bat_power)
                    else:
                        total_power -= sum(bat_power)
                    get_bat_value_store(1).set(BatState(power=sum(total_power), soc=mean(soc_bat)))
                get_inverter_value_store(num).set(InverterState(counter=total_energy,
                                                                power=min(0, total_power), currents=total_currents))
        else:
            inv = create_inverter(int(slave_id0))
            with SingleComponentUpdateContext(inv.component_info):
                state = inv.read_state()
                total_power = state.power * -1
                total_energy = state.counter

                if batwrsame == 1:
                    zweiterspeicher = 0
                    bat_power, _ = get_bat_state()
                    total_power -= sum(bat_power)

                device_config = get_default_config()
                device_config["ip_address"] = ip2address
                dev = Device(device_config)
                inv = create_inverter(int(slave_id0))
                state = inv.read_state()
                total_power -= state.power
                total_energy += state.counter
                if extprodakt:
                    state = get_external_inverter_state(dev, int(slave_id0))
                    total_power -= state.power
                get_inverter_value_store(num).set(InverterState(counter=total_energy, power=total_power))

    elif component_type == "bat":
        with SingleComponentUpdateContext(ComponentInfo(0, "Solaredge Speicher", "bat")):
            power_bat, soc_bat = get_bat_state()
            get_bat_value_store(1).set(BatState(power=sum(power_bat), soc=mean(soc_bat)))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
