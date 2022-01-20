#!/usr/bin/env python3
""" Modul zum Auslesen von Alpha Ess Speichern, Zählern und Wechselrichtern.
"""
from typing import Dict, List, Union, Optional

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.studer import bat
from modules.studer import inverter


def get_default_config() -> dict:
    return {
        "name": "Studer",
        "type": "studer",
        "id": 0,
        "configuration":
        {
            "ip_address": "192.168.193.15"
        }
    }


studer_component_classes = Union[bat.StuderBat, inverter.StuderInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.StuderBat,
        "inverter": inverter.StuderInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, studer_component_classes]
        try:
            ip_address = device_config["configuration"]["ip_address"]
            self.client = modbus.ModbusClient(ip_address, 502)
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                component_config, self.client))
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


def read_legacy(ip_address: str, component_config: dict, id: Optional[int], **kwargs):
    component_config["id"] = id
    component_config["configuration"].update(kwargs)
    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
    dev = Device(device_config)
    dev.add_component(component_config)
    dev.update()


def read_legacy_bat(ip_address: str, num: Optional[int]):
    read_legacy(ip_address, bat.get_default_config(), num)


def read_legacy_inverter(ip_address: str, vc_count: int, vc_type: str, num: Optional[int]):
    read_legacy(ip_address, inverter.get_default_config(), num, vc_count=vc_count, vc_type=vc_type)


def main(argv: List[str]):
    run_using_positional_cli_args({"bat": read_legacy_bat, "inverter": read_legacy_inverter}, argv)
