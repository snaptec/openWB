from typing import List, Union

try:
    from ..common import connect_tcp
    from ..common import abstract_device
    from ...helpermodules import log
    from . import counter
    from. import inverter
except:
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import log
    from modules.common import connect_tcp
    from modules.common import abstract_device
    import counter
    import inverter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit",
        "type": "openwb",
        "id": 0
    }


class Device(abstract_device.AbstractDevice):
    _COMPONENT_TYPE_TO_CLASS = {
        # "bat": ,
        "counter": counter.EvuKit,
        "inverter": inverter.PvKit
    }

    def __init__(self, device: dict) -> None:
        try:
            super().__init__(device, client=None)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])

    def add_component(self, component_config: dict) -> None:
        self.instantiate_component(component_config, self.component_factory(component_config["type"]))

    def component_factory(self, component_type: str) -> Union[counter.EvuKit, inverter.PvKit]:
        try:
            if component_type not in self._COMPONENT_TYPE_TO_CLASS:
                raise Exception("illegal component type "+component_type+". Allowed values: "+','.join(self._COMPONENT_TYPE_TO_CLASS.keys()))
            
            if component_type == "counter":
                ip_address = "192.168.193.15"
                port = 8899
                self.client = connect_tcp.ConnectTcp(self.data["config"]["id"], ip_address, port)
                return self._COMPONENT_TYPE_TO_CLASS[component_type]
            elif component_type == "inverter":
                ip_address = "192.168.193.13"
                port = 8899
                self.client = connect_tcp.ConnectTcp(self.data["config"]["id"], ip_address, port)
                return self._COMPONENT_TYPE_TO_CLASS[component_type]
            # elif component_type == "bat":
            #     pass
        except:
            log.MainLogger().exception("Fehler im Modul "+self.data["config"]["name"])


def read_legacy(argv: List[str]):
    """ Ausführung des Moduls als Python-Skript
    """
    try:
        _COMPONENT_TYPE_TO_MODULE = {
            # "bat": ,
            "counter": counter,
            "inverter": inverter
        }
        component_type = sys.argv[1]
        version = int(sys.argv[2])
        try:
            num = int(argv[3])
        except:
            num = None

        default = get_default_config()
        dev = Device(default)

        if component_type in _COMPONENT_TYPE_TO_MODULE:
            component_default = _COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
        else:
            raise Exception("illegal component type "+component_type+". Allowed values: "+','.join(_COMPONENT_TYPE_TO_MODULE.keys()))
        component_default["id"] = num
        component_default["configuration"]["version"] = version
        dev.add_component(component_default)

        log.MainLogger().debug('openWB Version: ' + str(version))

        dev.update_values()
    except:
        log.MainLogger().exception("Fehler im Modul openwb")


if __name__ == "__main__":
    read_legacy(sys.argv)
