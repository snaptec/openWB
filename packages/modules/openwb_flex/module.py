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
    def __init__(self, device: dict) -> None:
        try:
            self.data = {}
            self.data["config"] = device
            self.data["simulation"] = {}
            if device["components"]["component0"]["type"] == "counter":
                self.mod = evu_kit.EvuKitFlex(device)
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+device["name"], e)

    def read(self):
        try:
            self.mod.read()
        except Exception as e:
            log.MainLogger().error("Fehler im Modul "+self.data["config"]["name"], e)


def read_legacy(argv: List):
    """ Ausführung des Moduls als Python-Skript
    """
    try:
        component_type = str(argv[1])
        version = int(argv[2])
        ip_address = str(argv[3])
        port = int(argv[4])
        id = int(argv[5])

        device0 = {"name": "OpenWB-Kit", "type": "openwb_flex", "id": 0, "configuration": {"ip_address": ip_address, "port": port},
                   "components": {"component0": {"name": "EVU-Kit flex", "type": component_type, "id": 0, "configuration": {"version": version, "id": id}}}}
        mod = Module(device0)

        log.MainLogger().debug('openWB Version: ' + str(version))
        log.MainLogger().debug('Counter-Module EVU-Kit IP-Adresse: ' + str(ip_address))
        log.MainLogger().debug('Counter-Module EVU-Kit Port: ' + str(port))
        log.MainLogger().debug('Counter-Module EVU-Kit ID: ' + str(id))

        mod.read()
    except Exception as e:
        log.MainLogger().error("Fehler im Modul openwb_flex", e)


if __name__ == "__main__":
    read_legacy(sys.argv)
