#!/usr/bin/env python3
import itertools
import logging
from typing import Dict, Optional, Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store
from modules.sma_webbox import inverter as webbox_inverter
from modules.sma_sunny_boy import bat, bat_smart_energy, counter, inverter
from modules.sma_sunny_boy.inverter_version import SmaInverterVersion

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "SMA Sunny Boy",
        "type": "sma_sunny_boy",
        "id": 0,
        "configuration": {
            "ip_address": None
        }
    }


sma_modbus_tcp_component_classes = Union[
    bat.SunnyBoyBat,
    bat_smart_energy.SunnyBoySmartEnergyBat,
    counter.SmaSunnyBoyCounter,
    inverter.SmaModbusTcpInverter
]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.SunnyBoyBat,
        "bat_smart_energy": bat_smart_energy.SunnyBoySmartEnergyBat,
        "counter": counter.SmaSunnyBoyCounter,
        "inverter": inverter.SmaModbusTcpInverter
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, sma_modbus_tcp_component_classes]
        try:
            self.device_config = device_config
            ip_address = device_config["configuration"]["ip_address"]
            self.client = modbus.ModbusTcpClient_(ip_address, 502)
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"],
                component_config,
                self.client))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components.values():
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(component.component_info):
                    component.update()
        else:
            log.warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "bat_smart_energy": bat_smart_energy,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str,
                ip1: str,
                webbox: Optional[int] = None,
                ip2: Optional[str] = None,
                ip3: Optional[str] = None,
                ip4: Optional[str] = None,
                version: Optional[int] = None,
                hybrid: Optional[int] = None,
                num: Optional[int] = None) -> None:

    log.debug("SMA Modbus Ip-Adresse: "+ip1)
    log.debug("SMA Modbus Webbox: "+str(webbox))
    log.debug("SMA Modbus weitere IPs: "+str(ip2)+", "+str(ip3)+", "+str(ip4))
    log.debug("SMA Modbus Version: "+str(version))
    if component_type in COMPONENT_TYPE_TO_MODULE:
        if component_type == "inverter":
            read_inverter(ip1, webbox, ip2, ip3, ip4, version, hybrid, num)
            return
        else:
            component_config = COMPONENT_TYPE_TO_MODULE[
                component_type].get_default_config()
            component_config["id"] = None
            device_config = get_default_config()
            device_config["configuration"]["ip_address"] = ip1
            dev = Device(device_config)
            dev.add_component(component_config)
            dev.update()
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))


def read_inverter(ip1: str, webbox: int, ip2: str, ip3: str, ip4: str, version: int, hybrid: int, num: int):
    def create_webbox_inverter(address: str):
        config = webbox_inverter.get_default_config()
        config["id"] = num
        return webbox_inverter.SmaWebboxInverter(0, address, config)

    def create_modbus_inverter(address: str):
        config = inverter.get_default_config()
        config["id"] = num
        config["configuration"]["version"] = SmaInverterVersion(version)
        config["configuration"]["hybrid"] = bool(hybrid)
        return inverter.SmaModbusTcpInverter(0, config, modbus.ModbusTcpClient_(address, 502))

    inverter1 = (create_webbox_inverter if webbox else create_modbus_inverter)(ip1)
    inverters_additional = (create_modbus_inverter(address) for address in [ip2, ip3, ip4] if address != "none")
    # In legacy we were able to configure multiple IP-Addresses for a single SMA-component, effectively creating a
    # virtual component that represents the sum of its subcomponents. This was probably done in order to circumvent
    # the limitation to have a maximum of two inverters configured in legacy.
    # Since openWB 2 does not have a limitation on the number of inverters we do not implement this there. However
    # we still need to implement this for the read_legacy-bridge.
    # Here we act like we only update the first inverter, while we actually query all inverters and sum them up:
    with SingleComponentUpdateContext(inverter1.component_info):
        total_power = 0
        total_energy = 0
        for inv in itertools.chain((inverter1,), inverters_additional):
            state = inv.read()
            total_power += state.power
            total_energy += state.exported
        if hybrid == 1:
            bat_default = bat.get_default_config()
            bat_comp = bat.SunnyBoyBat(0, bat_default, modbus.ModbusTcpClient_(ip1, 502))
            bat_state = bat_comp.read()
            total_power -= bat_state.power
            total_energy = total_energy+bat_state.imported-bat_state.exported
        get_inverter_value_store(num).set(InverterState(exported=total_energy, power=total_power))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
