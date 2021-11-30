#!/usr/bin/env python3
""" Modul zum Auslesen von Alpha Ess Speichern, Zählern und Wechselrichtern.
"""
import sys
from typing import List, Union

from helpermodules import log
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_state import SingleComponentUpdateContext
from modules.alpha_ess import bat
from modules.alpha_ess import counter
from modules.alpha_ess import inverter


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS",
        "type": "alpha_ess",
        "id": None
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.AlphaEssBat,
        "counter": counter.AlphaEssCounter,
        "inverter": inverter.AlphaEssInverter
    }

    _components = []  # type: List[Union[bat.AlphaEssBat, counter.AlphaEssCounter, inverter.AlphaEssInverter]]

    def __init__(self, device_config: dict) -> None:
        try:
            self.client = modbus.ModbusClient("192.168.193.125", 8899)
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components.append(self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"], component_config, self.client))

    def get_values(self) -> None:
        log.MainLogger().debug("Start device reading" + str(self._components))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(component.component_info):
                    component.update()
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
    version = int(argv[2])
    try:
        num = int(argv[3])
    except IndexError:
        num = None

    device_config = get_default_config()
    device_config["id"] = 0
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    dev.add_component(component_config)

    log.MainLogger().debug('alpha_ess Version: ' + str(version))

    dev.get_values()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception:
        log.MainLogger().exception("Fehler im Alpha Ess Skript")
