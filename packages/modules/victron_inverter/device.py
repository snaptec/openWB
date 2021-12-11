#!/usr/bin/env python3
import sys
from typing import Dict, List

from helpermodules import log
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.victron_inverter import inverter


def get_default_config() -> dict:
    return {
        "name": "Wechselrichter Victron",
        "type": "victron_inverter",
        "id": 0,
        "configuration": {}
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "inverter": inverter.VictronInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, inverter.VictronInverter]
        try:
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (
                self.COMPONENT_TYPE_TO_CLASS[component_type](self.device_config["id"], component_config))
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


def read_legacy(argv: List[str]) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "inverter": inverter
    }
    component_type = argv[1]
    ip_address = argv[2]
    modbus_id = argv[3]
    mppt = argv[4]
    try:
        num = int(argv[5])
    except IndexError:
        num = None

    device_config = get_default_config()
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )

    component_config["id"] = num
    component_config["configuration"]["ip_address"] = ip_address
    component_config["configuration"]["modbus_id"] = modbus_id
    component_config["configuration"]["mppt"] = mppt
    dev.add_component(component_config)

    log.MainLogger().debug('Victron IP-Adresse: ' + str(ip_address))
    log.MainLogger().debug('Victron Modbus-ID: ' + str(modbus_id))
    log.MainLogger().debug('Victron MPPT: ' + str(mppt))
    dev.update()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception:
        log.MainLogger().exception("Fehler im Victron Skript")
