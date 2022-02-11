#!/usr/bin/env python3
import re
from typing import Dict, Union, List

from urllib3.util import parse_url

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.http import bat
from modules.http import counter
from modules.http import inverter


def get_default_config() -> dict:
    return {
        "name": "HTTP",
        "type": "http",
        "id": 0,
        "configuration": {
            "protocol": "http",
            "domain": "192.168.193.15"
            # ToDo: add port
        }
    }


http_component_classes = Union[bat.HttpBat, counter.HttpCounter, inverter.HttpInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.HttpBat,
        "counter": counter.HttpCounter,
        "inverter": inverter.HttpInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, http_component_classes]
        try:
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            domain = self.device_config["configuration"]["protocol"] + \
                "://" + self.device_config["configuration"]["domain"]
            self._components["component"+str(component_config["id"])] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                component_config, domain)
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
    log.MainLogger().debug(
        'Http Konfiguration: ' + str(device_config["configuration"]) + str(component_config["configuration"])
    )
    device.update()


def create_legacy_device_config(url: str):
    parsed_url = parse_url(url)
    device_config = get_default_config()
    device_config["configuration"]["protocol"] = parsed_url.scheme
    device_config["configuration"]["domain"] = parsed_url.hostname+":" + \
        str(parsed_url.port) if parsed_url.port else parsed_url.hostname
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


def read_legacy_inverter(power_path: str, counter_path: str, num: int):
    component_config = inverter.get_default_config()
    component_config["id"] = num
    component_config["configuration"] = create_paths_dict(
        power_path=power_path,
        counter_path=counter_path,
    )
    run_device_legacy(create_legacy_device_config(power_path), component_config)


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )
