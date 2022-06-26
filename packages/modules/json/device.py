#!/usr/bin/env python3
import logging
from typing import Dict, List, Union, Optional

from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext
from modules.json import bat
from modules.json import counter
from modules.json import inverter

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "Json",
        "type": "json",
        "id": 0,
        "configuration": {
            "url": None
        }
    }


class JsonConfiguration:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def from_dict(device_config: dict):
        keys = ["url"]
        try:
            values = [device_config[key] for key in keys]
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return JsonConfiguration(*values)


class Json:
    def __init__(self, name: str, type: str, id: int, configuration: JsonConfiguration) -> None:
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
                    values.append(JsonConfiguration.from_dict(device_config[key]))
                else:
                    values.append(device_config[key])
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return Json(*values)


json_component_classes = Union[bat.JsonBat, counter.JsonCounter, inverter.JsonInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.JsonBat,
        "counter": counter.JsonCounter,
        "inverter": inverter.JsonInverter
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, json_component_classes]
        try:
            self.device_config = device_config \
                if isinstance(device_config, Json) \
                else Json.from_dict(device_config)
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            with MultiComponentUpdateContext(self.components):
                response = req.get_http_session().get(self.device_config.configuration.url, timeout=5)
                for component in self.components:
                    self.components[component].update(response.json())
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(url: str, component_config: dict, num: Optional[int] = None, **kwargs) -> None:
    component_config["configuration"].update(kwargs)
    component_config["id"] = num

    device_config = get_default_config()
    device_config["configuration"]["url"] = url
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


def read_legacy_inverter(ip_address: str, jq_power: str, jq_exported: str, num: int):
    read_legacy(ip_address, inverter.get_default_config(), num, jq_power=jq_power, jq_exported=jq_exported)


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )
