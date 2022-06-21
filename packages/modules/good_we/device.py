#!/usr/bin/env python3
import logging
from typing import Dict, List, Union, Optional

from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.good_we import bat
from modules.good_we import counter
from modules.good_we import inverter

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "GoodWe",
        "type": "good_we",
        "id": 0,
        "configuration":
        {
            "ip_address": None,
            "id": 247
        }
    }


good_we_component_classes = Union[bat.GoodWeBat, counter.GoodWeCounter, inverter.GoodWeInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.GoodWeBat,
        "counter": counter.GoodWeCounter,
        "inverter": inverter.GoodWeInverter
    }

    def __init__(self, device_config: dict) -> None:
        self.components = {}  # type: Dict[str, good_we_component_classes]
        try:
            ip_address = device_config["configuration"]["ip_address"]
            self.client = modbus.ModbusClient(ip_address, 502)
            self.device_config = device_config
        except Exception:
            log.exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["configuration"]["id"], component_config, self.client))
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


def read_legacy(component_type: str, ip_address: str, id: int, num: Optional[int]) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
    device_config["configuration"]["id"] = id
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

    log.debug('GoodWe IP-Adresse: ' + ip_address)
    log.debug('GoodWe ID: ' + str(id))

    dev.update()
    dev.client.close_connection()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
