#!/usr/bin/env python3
""" Modul zum Auslesen von Alpha Ess Speichern, Zählern und Wechselrichtern.
"""
from typing import List

if __name__ == "__main__":
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.alpha_ess import bat
    from modules.alpha_ess import counter
    from modules.alpha_ess import inverter
else:
    from ...helpermodules import log
    from ..common import connect_tcp
    from . import bat
    from . import counter
    from . import inverter


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS",
        "type": "alpha_ess",
        "id": None
    }


class Device():
    def __init__(self, device_config: dict) -> None:
        try:
            super().__init__()
            self.data = {}
            self.data["config"] = device_config
            self.client = connect_tcp.ConnectTcp(self.data["config"]["name"], self.data["config"]["id"], "192.168.193.125", 8899)
            self.data["components"] = {}
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def add_component(self, component_config: dict) -> None:
        try:
            factory = self.__component_factory(component_config["type"])
            self.data["components"]["component"+str(component_config["id"])] = factory(self.client, component_config)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def __component_factory(self, component_type: str):
        try:
            if component_type == "bat":
                return bat.AlphaEssBat
            elif component_type == "counter":
                return counter.AlphaEssCounter
            elif component_type == "inverter":
                return inverter.AlphaEssInverter
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def read(self):
        try:
            if len(self.data["components"]) > 0:
                for component in self.data["components"]:
                    self.data["components"][component].read()
            else:
                log.MainLogger().warning(self.data["config"]["name"]+": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden.")
        except Exception as e:
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
    except Exception as e:
        log.MainLogger().exception("Fehler im Modul Alpha ESS")


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception as e:
        log.MainLogger().exception("Fehler im Alpha Ess Skript")
