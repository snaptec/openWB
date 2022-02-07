#!/usr/bin/env python3
import time
from typing import Dict, Union, List

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.huawei import bat
from modules.huawei import counter
from modules.huawei import inverter


def get_default_config() -> dict:
    return {
        "name": "Huawei",
        "type": "huawei",
        "id": 0,
        "configuration": {
            "ip_address": "192.168.193.15",
            "modbus_id": 1
        }
    }


huawei_component_classes = Union[bat.HuaweiBat, counter.HuaweiCounter, inverter.HuaweiInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.HuaweiBat,
        "counter": counter.HuaweiCounter,
        "inverter": inverter.HuaweiInverter
    }

    def __init__(self, device_config: dict) -> None:
        self._components = {}  # type: Dict[str, huawei_component_classes]
        try:
            ip_address = device_config["configuration"]["ip_address"]
            self.client = modbus.ModbusClient(ip_address, 502)
            self.client.delegate.connect()
            time.sleep(7)
            self.device_config = device_config
        except Exception:
            log.MainLogger().exception("Fehler im Modul "+device_config["name"])

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+component_type] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"],
                component_config, self.client,
                self.device_config["configuration"]["modbus_id"]))
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


def read_legacy(ip_address: str, modbus_id: int, read_counter: str = "False", read_battery: str = "False") -> None:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }

    components_to_read = ["inverter"]
    if read_counter.lower() == "true":
        components_to_read.append("counter")
    if read_battery.lower() == "true":
        components_to_read.append("bat")
    log.MainLogger().debug("components to read: " + str(components_to_read))

    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
    device_config["configuration"]["modbus_id"] = modbus_id
    dev = Device(device_config)
    for component_type in components_to_read:
        if component_type in COMPONENT_TYPE_TO_MODULE:
            component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(COMPONENT_TYPE_TO_MODULE.keys())
            )
        if component_type == "counter" or component_type == "bat":
            num = None
        else:
            num = 1
        component_config["id"] = num
        dev.add_component(component_config)

    log.MainLogger().debug('Huawei IP-Adresse: ' + str(ip_address))
    log.MainLogger().debug('Huawei Modbus-ID: ' + str(modbus_id))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
