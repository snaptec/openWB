from typing import List

try:
    from ...helpermodules import log
    from ..common import connect_tcp
    from ..common import misc_device
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
    import counter
    import inverter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit",
        "type": "openwb_flex",
        "id": None,
        "configuration":
        {
            "ip_address": "192.168.193.15",
            "port": "8899"
        }
    }


class Device(misc_device.MiscDevice):
    def __init__(self, device: dict) -> None:
        try:
            ip_address = device["configuration"]["ip_address"]
            port = device["configuration"]["port"]
            client = connect_tcp.ConnectTcp(device["id"], ip_address, port)
            super().__init__(device, client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+device["name"])


    def component_factory(self, component_type: str):
        try:
            if component_type == "bat":
                pass
            elif component_type == "counter":
                return counter.EvuKitFlex
            elif component_type == "inverter":
                return inverter.PvKitFlex
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])


def read_legacy(argv: List):
    """ Ausführung des Moduls als Python-Skript
    """
    try:
        log.MainLogger().debug('Start reading flex')
        component_type = str(argv[1])
        version = int(argv[2])
        ip_address = str(argv[3])
        port = int(argv[4])
        id = int(argv[5])
        try:
            num = int(argv[6])
        except:
            num = None

        default = get_default_config()
        default["id"] = 0
        default["configuration"]["ip_address"] = ip_address
        default["configuration"]["port"] = port
        dev = Device(default)
        component_default = globals()[component_type].get_default_config()
        component_default["id"] = num
        component_default["configuration"]["version"] = version
        component_default["configuration"]["id"] = id
        dev.add_component(component_default)

        log.MainLogger().debug('openWB Version: ' + str(version))
        log.MainLogger().debug('openWB-Kit IP-Adresse: ' + str(ip_address))
        log.MainLogger().debug('openWB-Kit Port: ' + str(port))
        log.MainLogger().debug('openWB-Kit ID: ' + str(id))

        dev.read()
    except Exception as e:
        log.MainLogger().exception("Fehler im Modul openwb_flex")


if __name__ == "__main__":
    read_legacy(sys.argv)
