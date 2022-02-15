#!/usr/bin/env python3
""" Modul zum Auslesen von sonnenBatterie Speichern.
"""
from typing import Dict, Union, List

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import InverterState
from modules.sma_modbus_tcp import inverter_modbus_tcp
from modules.sma_modbus_tcp import inverter_webbox
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext, SingleComponentUpdateContext
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Modbus TCP",
        "type": "sma_modbus_tcp",
        "id": 0,
        "configuration": {
            "ip": ""
        }
    }


sma_modbus_tcp_component_classes = Union[
    inverter_webbox.SmaWebboxInverter,
    inverter_modbus_tcp.SmaModbusTcpInverter
]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "inverter_modbus_tcp": inverter_modbus_tcp.SmaModbusTcpInverter,
        "inverter_webbox": inverter_webbox.SmaWebboxInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, sma_modbus_tcp_component_classes]
        try:
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["configuration"]["ip"],
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.MainLogger().debug("Start device reading " + str(self._components))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self._components[component].component_info):
                    self._components[component].update()
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(ip1: str, webbox: int, ip2: str, ip3: str, ip4: str, num: int) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "inverter_modbus_tcp": inverter_modbus_tcp,
        "inverter_webbox": inverter_webbox
    }
    device_config = get_default_config()
    device_config["configuration"]["ip"] = ip1
    dev = Device(device_config)
    if webbox == 1:
        component_config = COMPONENT_TYPE_TO_MODULE["inverter_webbox"].get_default_config()
    else:
        component_config = COMPONENT_TYPE_TO_MODULE["inverter_modbus_tcp"].get_default_config()
    component_config["id"] = 0
    dev.add_component(component_config)
    log.MainLogger().debug('SMA ModbusTCP address: ' + ip1)
    log.MainLogger().debug('SMA ModbusTCP Webbox: ' + str(webbox))

    i = 1
    for ip in [ip2, ip3, ip4]:
        if ip != "none":
            component_config = COMPONENT_TYPE_TO_MODULE["inverter_modbus_tcp"].get_default_config()
            component_config["id"] = i
            dev.add_component(component_config)
            log.MainLogger().debug('SMA ModbusTCP address: ' + ip)
            i += 1

    power_total, energy_total = 0, 0
    with MultiComponentUpdateContext(dev._components):
        for comp in dev._components.values():
            inverter_state = comp.read_inverter_state()
            power_total += inverter_state.power
            energy_total += inverter_state.counter

    get_inverter_value_store(num).set(InverterState(counter=energy_total, power=power_total))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
