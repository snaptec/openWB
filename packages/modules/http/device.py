#!/usr/bin/env python3
import logging
import re
from typing import Dict, Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.http import bat
from modules.http import counter
from modules.http import inverter

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "HTTP",
        "type": "http",
        "id": 0,
        "configuration": {
            "url": None
        }
    }


class HttpConfiguration:
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
        return HttpConfiguration(*values)


class Http:
    def __init__(self, name: str, type: str, id: int, configuration: HttpConfiguration) -> None:
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
                    values.append(HttpConfiguration.from_dict(device_config[key]))
                else:
                    values.append(device_config[key])
        except KeyError as e:
            raise Exception(
                "Illegal configuration <{}>: Expected object with properties: {}".format(device_config, keys)
            ) from e
        return Http(*values)


http_component_classes = Union[bat.HttpBat, counter.HttpCounter, inverter.HttpInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.HttpBat,
        "counter": counter.HttpCounter,
        "inverter": inverter.HttpInverter
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, http_component_classes]
        try:
            self.device_config = device_config \
                if isinstance(device_config, Http) \
                else Http.from_dict(device_config)
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config, self.device_config.configuration.url)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self.components[component].component_info):
                    self.components[component].update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def create_paths_dict(**kwargs):
    regex = re.compile("^(https?://[^/]+)(.*)")
    result = {}
    host_scheme = None
    for key, path in kwargs.items():
        if path == "none":
            result[key] = "none"
        else:
            match = regex.search(path)
            if match is None:
                raise Exception("Invalid URL <" + path + ">: Absolute HTTP or HTTPS URL required")
            if host_scheme is None:
                host_scheme = match.group(1)
            elif host_scheme != match.group(1):
                raise Exception("All URLs must have the same scheme and host. However URLs are: " + str(kwargs))
            result[key] = match.group(2)
    return result


def run_device_legacy(device_config: dict, component_config: dict):
    device = Device(device_config)
    device.add_component(component_config)
    log.debug(
        'Http Konfiguration: ' + str(device_config["configuration"]) + str(component_config["configuration"])
    )
    device.update()


def create_legacy_device_config(url: str):
    regex = re.compile("^(https?://[^/]+)(.*)")
    match = regex.search(url)
    if match is None:
        raise Exception("Invalid URL <" + url + ">: Absolute HTTP or HTTPS URL required")
    host_scheme = match.group(1)
    device_config = get_default_config()
    device_config["configuration"]["url"] = host_scheme
    return device_config


def read_legacy_bat(power_path: str, imported_path: str, exported_path: str, soc_path: str) -> None:
    component_config = bat.get_default_config()
    component_config["configuration"] = create_paths_dict(
        power_path=power_path,
        imported_path=imported_path,
        exported_path=exported_path,
        soc_path=soc_path,
    )
    run_device_legacy(create_legacy_device_config(power_path), component_config)


def read_legacy_counter(power_path: str, imported_path: str, exported_path: str, current_l1_path: str,
                        current_l2_path: str, current_l3_path: str):
    component_config = counter.get_default_config()
    component_config["configuration"] = create_paths_dict(
        power_path=power_path,
        imported_path=imported_path,
        exported_path=exported_path,
        current_l1_path=current_l1_path,
        current_l2_path=current_l2_path,
        current_l3_path=current_l3_path,
    )
    run_device_legacy(create_legacy_device_config(power_path), component_config)


def read_legacy_inverter(power_path: str, exported_path: str, num: int):
    component_config = inverter.get_default_config()
    component_config["id"] = num
    component_config["configuration"] = create_paths_dict(
        power_path=power_path,
        exported_path=exported_path,
    )
    run_device_legacy(create_legacy_device_config(power_path), component_config)


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )
