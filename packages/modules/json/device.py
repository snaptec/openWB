#!/usr/bin/env python3
import logging
from typing import Dict, List, Union, Optional
from urllib3.util import parse_url

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
            "protocol": "http",
            "domain": None,
            "port": 80
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
        self.components = {}  # type: Dict[str, json_component_classes]
        try:
            self.device_config = device_config
            port = self.device_config["configuration"]["port"]
            self.domain = self.device_config["configuration"]["protocol"] + \
                "://" + self.device_config["configuration"]["domain"] + \
                ":" + str(port) if port else ""
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"], component_config)
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            with MultiComponentUpdateContext(self.components):
                response = req.get_http_session().get(self.domain, timeout=5)
                for component in self.components:
                    self.components[component].update(response.json())
        else:
            log.warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(ip_address: str, component_config: dict, num: Optional[int] = None, **kwargs) -> None:
    component_config["configuration"].update(kwargs)
    component_config["id"] = num

    parsed_url = parse_url(ip_address)
    device_config = get_default_config()
    device_config["configuration"]["protocol"] = parsed_url.scheme
    device_config["configuration"]["domain"] = parsed_url.hostname
    device_config["configuration"]["port"] = int(parsed_url.port)

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
