#!/usr/bin/env python3
from typing import Dict, List, Union, Optional

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext
from modules.json import bat
from modules.json import counter
from modules.json import inverter


def get_default_config() -> dict:
    return {
        "name": "Json",
        "type": "json",
        "id": 0,
        "configuration": {
            "ip_address": "192.168.193.15"
            # ToDo: add protocol
            # ToDo: add port
        }
    }


json_component_classes = Union[bat.JsonBat, counter.JsonCounter, inverter.JsonInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.JsonBat,
        "counter": counter.JsonCounter,
        "inverter": inverter.JsonInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, json_component_classes]
        try:
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"], component_config)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.MainLogger().debug("Start device reading " + str(self._components))
        if self._components:
            with MultiComponentUpdateContext(self._components):
                response = req.get_http_session().get(self.device_config["configuration"]["ip_address"], timeout=5)
                for component in self._components:
                    self._components[component].update(response.json())
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(ip_address: str, component_config: dict, num: Optional[int] = None, **kwargs) -> None:
    component_config["configuration"].update(kwargs)
    component_config["id"] = num

    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address

    dev = Device(device_config)
    dev.add_component(component_config)
    dev.update()


def read_legacy_bat(ip_address: str, jq_power: str, jq_soc: str):
    read_legacy(ip_address, bat.get_default_config(), jq_power=jq_power, jq_soc=jq_soc)


def read_legacy_counter(ip_address: str, jq_power: str, jq_imported: str, jq_exported: str):
    read_legacy(
        ip_address,
        counter.get_default_config(),
        jq_power=jq_power,
        jq_imported=jq_imported,
        jq_exported=jq_exported
    )


def read_legacy_inverter(ip_address: str, jq_power: str, jq_counter: str, num: int):
    read_legacy(ip_address, inverter.get_default_config(), num, jq_power=jq_power, jq_counter=jq_counter)


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )
