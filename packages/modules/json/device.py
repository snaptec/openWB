#!/usr/bin/env python3
import sys
from typing import Dict, List, Union

from helpermodules import log
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
        "configuration":
        {
            "ip_address": "192.168.193.15"
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


def read_legacy(argv: List[str]) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    component_type = argv[1]

    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = argv[2]
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    if component_type == "bat":
        component_config["configuration"] = {
            "jq_power": argv[3],
            "jq_soc": argv[4]
        }
        num = None
    elif component_type == "counter":
        component_config["configuration"] = {
            "jq_power": argv[3],
            "jq_imported": argv[4],
            "jq_exported": argv[5]
        }
        num = None
    else:
        component_config["configuration"] = {
            "jq_power": argv[3],
            "jq_counter": argv[4]
        }
        num = int(argv[5])

    component_config["id"] = num
    dev.add_component(component_config)

    log.MainLogger().debug('Json Konfiguration: ' + str(component_config["configuration"]))

    dev.update()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception:
        log.MainLogger().exception("Fehler im Json Skript")
