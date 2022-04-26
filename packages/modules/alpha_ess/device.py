#!/usr/bin/env python3
""" Modul zum Auslesen von Alpha Ess Speichern, Zählern und Wechselrichtern.
"""
from typing import Dict, Union, Optional, List

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.alpha_ess import bat
from modules.alpha_ess import counter
from modules.alpha_ess import inverter
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS",
        "type": "alpha_ess",
        "id": 0,
        "configuration": {
            "source": 0,  # 0: AlphaEss-Kit, 1: Hi5/10 mit variabler IP
            "version": 1,  # 0: <V1.23, 1: >= V1.23
            "ip_address": None
        }
    }


alpha_ess_component_classes = Union[bat.AlphaEssBat, counter.AlphaEssCounter, inverter.AlphaEssInverter]
default_unit_id = 85


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.AlphaEssBat,
        "counter": counter.AlphaEssCounter,
        "inverter": inverter.AlphaEssInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, alpha_ess_component_classes]
        try:
            if device_config["configuration"]["source"] == 0:
                self.client = modbus.ModbusClient("192.168.193.125", 8899)
            else:
                self.client = modbus.ModbusClient(device_config["configuration"]["ip_address"], 502)
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"],
                component_config,
                self.client,
                self.device_config["configuration"]))
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
                    self._components[component].update(unit_id=default_unit_id)
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, source: int, version: int, ip_address: str, num: Optional[int] = None) -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    device_config = get_default_config()
    device_config["configuration"]["source"] = source
    device_config["configuration"]["version"] = version
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

    log.MainLogger().debug('alpha_ess Version: ' + str(version))
    log.MainLogger().debug('alpha_ess IP-Adresse: ' + str(ip_address))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
