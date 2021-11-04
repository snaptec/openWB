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
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
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
    def __init__(self, device: dict) -> None:
        try:
            client = connect_tcp.ConnectTcp(device["id"], "192.168.193.125", 8899)
            super().__init__(device, client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+device["name"])

    def component_factory(self, component_type: str) -> Union[bat.AlphaEssBat, counter.AlphaEssCounter, inverter.AlphaEssInverter]:
        try:
            if component_type == "bat":
                return bat.AlphaEssBat
            elif component_type == "counter":
                return counter.AlphaEssCounter
            elif component_type == "inverter":
                return inverter.AlphaEssInverter
        except:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])


def read_legacy(argv: List):
    try:
        component_type = str(argv[1])
        version = int(argv[2])
        try:
            num = int(argv[3])
        except:
            num = None

        default = get_default_config()
        default["id"] = 0
        dev = Device(default)
        component_default = globals()[component_type].get_default_config()
        component_default["id"] = num
        component_default["configuration"]["version"] = version
        dev.add_component(component_default)

        log.MainLogger().debug('alpha_ess Version: ' + str(version))

        dev.read()
    except:
        log.MainLogger().exception("Fehler im Modul Alpha ESS")


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except:
        log.MainLogger().exception("Fehler im Alpha Ess Skript")
