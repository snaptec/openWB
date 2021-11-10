#!/usr/bin/env python3
""" Modul zum Auslesen von Alpha Ess Speichern, Zählern und Wechselrichtern.
"""
import sys
from typing import List, Union

try:
    from ...helpermodules import log
    from ..common import modbus
    from modules.common import abstract_device
    from . import bat
    from . import counter
    from . import inverter
except:
    from helpermodules import log
    from modules.common import modbus
    from modules.common import abstract_device
    from modules.alpha_ess import bat
    from modules.alpha_ess import counter
    from modules.alpha_ess import inverter


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS",
        "type": "alpha_ess",
        "id": None
    }


class Device(abstract_device.AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.AlphaEssBat,
        "counter": counter.AlphaEssCounter,
        "inverter": inverter.AlphaEssInverter
    }

    def __init__(self, device: dict) -> None:
        try:
            client = modbus.ModbusClient("192.168.193.125", 8899)
            super().__init__(device, client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+device["name"])

    def add_component(self, component_config: dict) -> None:
        self.instantiate_component(
            component_config, self.component_factory(component_config["type"]))


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
    except:
        num = None

    device_config = get_default_config()
    device_config["id"] = 0
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception("illegal component type "+component_type+". Allowed values: "+','.join(COMPONENT_TYPE_TO_MODULE.keys()))
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    dev.add_component(component_config)

    log.MainLogger().debug('alpha_ess Version: ' + str(version))

    dev.update_values()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except:
        log.MainLogger().exception("Fehler im Alpha Ess Skript")
