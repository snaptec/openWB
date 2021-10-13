from typing import List

try:
    from ...helpermodules import log
    from . import evu_kit
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    import evu_kit


class Module():
    def __init__(self, device_config: dict) -> None:
        try:
            self.data = {}
            self.data["config"] = device_config
            self.data["simulation"] = {}
            self.data["components"] = []
            for c in self.data["config"]["components"]:
                component = self.data["config"]["components"][c]
                if component["type"] == "bat":
                    pass
                elif component["type"] == "counter":
                    self.data["components"].append(evu_kit.EvuKit(self.data["config"]))
                elif component["type"] == "inverter":
                    pass
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["name"], e)

    def read(self):
        try:
            for component in self.data["components"]:
                component.read()
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["name"], e)


def read_legacy(argv: List):
    """ Ausführung des Moduls als Python-Skript
    """
    try:
        component_type = str(sys.argv[1])
        version = int(sys.argv[2])

        device0 = {"name": "OpenWB-Kit", "type": "openwb", "id": 0, "components": {"component0": {"name": "EVU-Kit", "type": component_type, "id": 0, "configuration": {"version": version}}}}
        mod = Module(device0)

        log.MainLogger().debug('openWB Version: ' + str(version))

        mod.read()
    except Exception as e:
        log.MainLogger().error("Fehler im Modul openwb", e)


if __name__ == "__main__":
    read_legacy(sys.argv)
