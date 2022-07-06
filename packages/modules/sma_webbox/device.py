#!/usr/bin/env python3
import logging
from typing import Dict

from modules.sma_webbox import inverter
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext


log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "SMA Webbox",
        "type": "sma_webbox",
        "id": 0,
        "configuration": {
            "ip": None
        }
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "inverter": inverter.SmaWebboxInverter
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, inverter.SmaWebboxInverter]
        try:
            self.device_config = device_config
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["configuration"]["ip"],
                component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components.values():
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(component.component_info):
                    component.update()
        else:
            log.warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )

# read_legacy in sma_modbus
