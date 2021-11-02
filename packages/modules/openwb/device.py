from typing import List

try:
    from ..common import connect_tcp
    from ...helpermodules import log
    from . import counter
    from. import inverter
except:
    from pathlib import Path
    import os
    import sys
    parentdir2 = str(Path(os.path.abspath(__file__)).parents[2])
    sys.path.insert(0, parentdir2)
    from helpermodules import log
    from modules.common import connect_tcp
    import counter
    import inverter


def get_default() -> dict:
    return {
        "name": "OpenWB-Kit",
        "type": "openwb",
        "id": None
    }


class Device():
    def __init__(self, device_config: dict) -> None:
        try:
            self.data = {}
            self.data["config"] = device_config
            self.data["components"] = {}
            ip_address = "192.168.193.15"
            port = "8899"
            self.client = connect_tcp.ConnectTcp(self.data["config"]["name"], self.data["config"]["id"], ip_address, port)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def add_component(self, component_config: dict) -> None:
        try:
            if component_config["type"] == "counter":
                self.data["components"]["component"+str(component_config["id"])] = counter.EvuKit(self.data["config"]["id"], component_config, self.client)
            elif component_config["type"] == "inverter":
                self.data["components"]["component"+str(component_config["id"])] = inverter.PvKit(self.data["config"]["id"], component_config, self.client)
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
    """ Ausführung des Moduls als Python-Skript
    """
    try:
        component_type = str(sys.argv[1])
        version = int(sys.argv[2])
        try:
            num = int(argv[3])
        except:
            num = 0

        default = get_default()
        default["id"] = 0
        dev = Device(default)

        component_default = globals()[component_type].get_default()
        component_default["id"] = num
        component_default["configuration"]["version"] = version
        dev.add_component(component_default)

        log.MainLogger().debug('openWB Version: ' + str(version))

        dev.read()
    except Exception as e:
        log.MainLogger().exception("Fehler im Modul openwb")


if __name__ == "__main__":
    read_legacy(sys.argv)
