#!/usr/bin/env python3
""" Modul zum Auslesen von Alpha Ess Speichern, Zählern und Wechselrichtern.
"""
from typing import List, Union

try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from modules.common import misc_device
    from . import bat
    from . import counter
    from . import inverter
except:
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common import misc_device
    from modules.alpha_ess import bat
    from modules.alpha_ess import counter
    from modules.alpha_ess import inverter


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS",
        "type": "alpha_ess",
        "id": None
    }


class Device(misc_device.MiscDevice):
    _COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.AlphaEssBat,
        "counter": counter.AlphaEssCounter,
        "inverter": inverter.AlphaEssInverter
    }

    def __init__(self, device: dict) -> None:
        try:
            client = connect_tcp.ConnectTcp(device["id"], "192.168.193.125", 8899)
            super().__init__(device, client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+device["name"])

    def add_component(self, component_config: dict) -> None:
        self.instantiate_component(component_config, self.component_factory(component_config["type"]))


def read_legacy(argv: List[str]) -> None:
    try:
        _COMPONENT_TYPE_TO_MODULE = {
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

        default = get_default_config()
        default["id"] = 0
        dev = Device(default)
        if component_type in _COMPONENT_TYPE_TO_MODULE:
            component_default = _COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
        else:
            raise Exception("illegal component type "+component_type+". Allowed values: "+','.join(_COMPONENT_TYPE_TO_MODULE.keys()))
        component_default["id"] = num
        component_default["configuration"]["version"] = version
        dev.add_component(component_default)

        log.MainLogger().debug('alpha_ess Version: ' + str(version))

        dev.update_values()
    except:
        log.MainLogger().exception("Fehler im Modul Alpha ESS")


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except:
        log.MainLogger().exception("Fehler im Alpha Ess Skript")
