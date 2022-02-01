#!/usr/bin/env python3
from typing import Dict, List, Union, Optional

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.sungrow import bat
from modules.sungrow import counter
from modules.sungrow import inverter


def get_default_config() -> dict:
    return {
        "name": "Sungrow",
        "type": "sungrow",
        "id": 0,
        "configuration": {
            "ip_address": "192.168.193.15"
        }
    }


sungrow_component_classes = Union[bat.SungrowBat, counter.SungrowCounter, inverter.SungrowInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.SungrowBat,
        "counter": counter.SungrowCounter,
        "inverter": inverter.SungrowInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, sungrow_component_classes]
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
                self.device_config["id"], component_config, self.client))
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


def read_legacy(ip_address: str, component_config: dict, id: Optional[int] = None, **kwargs):
    component_config["id"] = id
    component_config["configuration"].update(kwargs)
    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
    dev = Device(device_config)
    dev.add_component(component_config)
    dev.update()


def read_legacy_bat(ip_address: str, num: Optional[int] = None):
    read_legacy(ip_address, bat.get_default_config(), num)


def read_legacy_counter(ip_address: str, version: int):
    read_legacy(ip_address, counter.get_default_config(), version=version)


def read_legacy_inverter(ip_address: str, num: int):
    read_legacy(ip_address, inverter.get_default_config(), num)


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )
