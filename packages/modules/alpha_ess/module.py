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


class module():
    def __init__(self, device_config: dict) -> None:
        try:
            super().__init__()
            self.data = {}
            self.data["config"] = device_config
            self.client = connect_tcp.ConnectTcp(self.data["config"]["name"], "192.168.193.125", 8899)
            self.data["components"] = []
            for c in self.data["config"]["components"]:
                component = self.data["config"]["components"][c]
                factory = self.__component_factory(component["type"])
                self.data["components"].append(factory(self.client, component))
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["name"], e)

    def __component_factory(self, component_type: str):
        try:
            if component_type == "bat":
                return bat.AlphaEssBat
            elif component_type == "counter":
                return counter.AlphaEssCounter
            elif component_type == "inverter":
                return inverter.AlphaEssInverter
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["name"], e)

    def read(self):
        try:
            log.MainLogger().debug("Komponenten von "+self.data["config"]["name"]+" auslesen.")
            for component in self.data["components"]:
                component.read()
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["name"], e)


def read_legacy(argv: List):
    try:
        component_type = str(argv[1])
        version = int(argv[2])

        device0 = {"name": "Alpha Ess", "type": "alpha_ess", "components": {"component0": {"name": "Alpha Ess "+component_type, "id": 0, "type": component_type, "configuration": {"version": version}}}}
        mod = module(device0)

        log.MainLogger().debug('alpha_ess Version: ' + str(version))

        mod.read()
    except Exception as e:
        log.MainLogger().error("Fehler im Modul Alpha Ess", e)


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception as e:
        log.MainLogger().error("Fehler im Alpha Ess-Skript", e)
