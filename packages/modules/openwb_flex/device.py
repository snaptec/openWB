from typing import List
import sys

try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common import abstract_device
    from . import counter
    from . import inverter
except:
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import log
    from modules.common import modbus
    from modules.common import abstract_device
    import counter
    import inverter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit",
        "type": "openwb_flex",
        "id": 0,
        "configuration":
        {
            "ip_address": "192.168.193.15",
            "port": "8899"
        }
    }


class Device(abstract_device.AbstractDevice):
    _COMPONENT_TYPE_TO_CLASS = {
        # "bat": ,
        "counter": counter.EvuKitFlex,
        "inverter": inverter.PvKitFlex
    }

    def __init__(self, device: dict) -> None:
        try:
            ip_address = device["configuration"]["ip_address"]
            port = device["configuration"]["port"]
            client = modbus.ModbusClient(ip_address, port)
            super().__init__(device, client)
        except Exception as e:
            log.MainLogger().exception("Fehler im Modul "+device["name"])

    def add_component(self, component_config: dict) -> None:
        self.instantiate_component(component_config, super().component_factory(component_config["type"]))


def read_legacy(argv: List[str]):
    """ Ausführung des Moduls als Python-Skript
    """
    try:
        _COMPONENT_TYPE_TO_MODULE = {
            # "bat": ,
            "counter": counter,
            "inverter": inverter
        }
        log.MainLogger().debug('Start reading flex')
        component_type = argv[1]
        version = int(argv[2])
        ip_address = argv[3]
        port = int(argv[4])
        id = int(argv[5])
        try:
            num = int(argv[6])
        except:
            num = None

        default = get_default_config()
        default["configuration"]["ip_address"] = ip_address
        default["configuration"]["port"] = port
        dev = Device(default)
        if component_type in _COMPONENT_TYPE_TO_MODULE:
            component_default = _COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
        else:
            raise Exception("illegal component type "+component_type+". Allowed values: "+','.join(_COMPONENT_TYPE_TO_MODULE.keys()))

        component_default["id"] = num
        component_default["configuration"]["version"] = version
        component_default["configuration"]["id"] = id
        dev.add_component(component_default)

        log.MainLogger().debug('openWB Version: ' + str(version))
        log.MainLogger().debug('openWB-Kit IP-Adresse: ' + str(ip_address))
        log.MainLogger().debug('openWB-Kit Port: ' + str(port))
        log.MainLogger().debug('openWB-Kit ID: ' + str(id))

        dev.update_values()
    except Exception as e:
        log.MainLogger().exception("Fehler im Modul openwb_flex")


if __name__ == "__main__":
    read_legacy(sys.argv)
