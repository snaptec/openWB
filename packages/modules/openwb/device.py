from typing import List, Union

try:
    from ..common import connect_tcp
    from ..common import misc_device
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
    from modules.common import misc_device
    import counter
    import inverter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit",
        "type": "openwb",
        "id": 0
    }


class Device(misc_device.MiscDevice):
    def __init__(self, device: dict) -> None:
        try:
            super().__init__(device, client=None)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def component_factory(self, component_type: str) -> Union[counter.EvuKit, inverter.PvKit]:
        try:
            if component_type == "bat":
                pass
            elif component_type == "counter":
                ip_address = "192.168.193.15"
                port = "8899"
                self.client = connect_tcp.ConnectTcp(self.data["config"]["id"], ip_address, port)
                return counter.EvuKit
            elif component_type == "inverter":
                ip_address = "192.168.193.13"
                port = "8899"
                self.client = connect_tcp.ConnectTcp(self.data["config"]["id"], ip_address, port)
                return inverter.PvKit
        except:
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
            num = None

        default = get_default_config()
        dev = Device(default)

        component_default = globals()[component_type].get_default_config()
        component_default["id"] = num
        component_default["configuration"]["version"] = version
        dev.add_component(component_default)

        log.MainLogger().debug('openWB Version: ' + str(version))

        dev.update_values()
    except:
        log.MainLogger().exception("Fehler im Modul openwb")


if __name__ == "__main__":
    read_legacy(sys.argv)
