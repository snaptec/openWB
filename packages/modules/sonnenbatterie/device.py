#!/usr/bin/env python3
""" Modul zum Auslesen von sonnenBatterie Speichern.
"""
import logging
from typing import Dict, Union, Optional, List

from helpermodules.cli import run_using_positional_cli_args
from modules.sonnenbatterie import bat
from modules.sonnenbatterie import counter
from modules.sonnenbatterie import inverter
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "SonnenBatterie",
        "type": "sonnenbatterie",
        "id": 0,
        "configuration": {
            "ip": None,
            "variant": 0
        }
    }


sonnenbatterie_component_classes = Union[
    bat.SonnenbatterieBat,
    counter.SonnenbatterieCounter,
    inverter.SonnenbatterieInverter
]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.SonnenbatterieBat,
        "counter": counter.SonnenbatterieCounter,
        "inverter": inverter.SonnenbatterieInverter
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, sonnenbatterie_component_classes]
        try:
            self.device_config = device_config
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"],
                self.device_config["configuration"]["ip"],
                self.device_config["configuration"]["variant"],
                component_config))
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
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, address: str, variant: int, num: Optional[int] = None) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    device_config = get_default_config()
    device_config["configuration"]["ip"] = address
    device_config["configuration"]["variant"] = variant
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config["id"] = num
    dev.add_component(component_config)
    log.debug('SonnenBatterie address: ' + address)
    log.debug('SonnenBatterie variant: ' + str(variant))
    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
