#!/usr/bin/env python3
from typing import Dict, Union, Optional, List

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext, SingleComponentUpdateContext
from modules.powerdog import counter
from modules.powerdog import inverter


def get_default_config() -> dict:
    return {
        "name": "Powerdog",
        "type": "powerdog",
        "id": 0,
        "configuration": {
            "ip_address": "192.168.193.15"
        }
    }


COMPONENT_TYPE_TO_MODULE = {
    "counter": counter,
    "inverter": inverter
}


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "counter": counter.PowerdogCounter,
        "inverter": inverter.PowerdogInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, Union[counter.PowerdogCounter, inverter.PowerdogInverter]]
        try:
            ip_address = device_config["configuration"]["ip_address"]
            self.client = modbus.ModbusClient(ip_address, 502)
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (
                self.COMPONENT_TYPE_TO_CLASS[component_type](self.device_config["id"], component_config, self.client))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.MainLogger().debug("Start device reading " + str(self._components))
        if len(self._components) == 1:
            for component in self._components:
                if isinstance(self._components[component], inverter.PowerdogInverter):
                    with SingleComponentUpdateContext(self._components[component].component_info):
                        self._components[component].update()
                else:
                    raise Exception(
                        "Wenn ein EVU-Zähler konfiguriert wurde, muss immer auch ein WR konfiguriert sein.")
        elif len(self._components) == 2:
            with MultiComponentUpdateContext(self._components):
                for component in self._components:
                    if isinstance(self._components[component], counter.PowerdogCounter):
                        home_consumption = self._components[component].update()
                    elif isinstance(self._components[component], inverter.PowerdogInverter):
                        inverter_power = self._components[component].update()
                    else:
                        raise Exception(
                            "illegal component type " + self._components[component].component_config["type"] +
                            ". Allowed values: " + ','.join(COMPONENT_TYPE_TO_MODULE.keys()))
                counter_power = home_consumption + inverter_power
                for component in self._components:
                    if isinstance(self._components[component], counter.PowerdogCounter):
                        self._components[component].set_counter_state(counter_power)
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine oder zu viele Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, ip_address: str, num: Optional[int] = None) -> None:
    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
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

    # Wenn der EVU-Zähler ausgelesen werden soll, wird auch noch der Inverter benötigt.
    if component_type in COMPONENT_TYPE_TO_MODULE and component_type == "counter":
        inverter_config = inverter.get_default_config()
        inverter_config["id"] = 1
        dev.add_component(inverter_config)

    log.MainLogger().debug('Powerdog IP-Adresse: ' + str(ip_address))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
