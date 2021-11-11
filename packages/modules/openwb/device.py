from typing import List, Union
import sys
try:
    from ..common import modbus
    from ..common import abstract_device
    from ...helpermodules import log
    from . import counter
    from. import inverter
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
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
    COMPONENT_TYPE_TO_CLASS = {
        # "bat": ,
        "counter": counter.EvuKit,
        "inverter": inverter.PvKit
    }

    def __init__(self, device: dict) -> None:
        try:
            super().__init__(device, client=None)
        except Exception:
            log.MainLogger().exception(
                "Fehler im Modul "+self.data["config"]["name"])

    def add_component(self, component_config: dict) -> None:
        self.instantiate_component(
            component_config, self.component_factory(component_config["type"]))

    def component_factory(self, component_type: str) -> Union[counter.EvuKit, inverter.PvKit]:
        try:
            if component_type == "counter":
                ip_address = "192.168.193.15"
                port = 8899
                self.client = modbus.ModbusClient(ip_address, port)
                return self.COMPONENT_TYPE_TO_CLASS[component_type]
            elif component_type == "inverter":
                ip_address = "192.168.193.13"
                port = 8899
                self.client = modbus.ModbusClient(ip_address, port)
                return self.COMPONENT_TYPE_TO_CLASS[component_type]
            # elif component_type == "bat":
            #     pass
            else:
                raise Exception("illegal component type "+component_type +
                                ". Allowed values: "+','.join(self.COMPONENT_TYPE_TO_CLASS.keys()))
        except Exception:
            log.MainLogger().exception(
                "Fehler im Modul "+self.data["config"]["name"])


def read_legacy(argv: List[str]):
    """ Ausführung des Moduls als Python-Skript
    """
    COMPONENT_TYPE_TO_MODULE = {
        # "bat": ,
        "counter": counter,
        "inverter": inverter
    }
    component_type = sys.argv[1]
    version = int(sys.argv[2])
    try:
        num = int(argv[3])
    except ValueError:
        num = None

    device_config = get_default_config()
    dev = Device(device_config)

    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config(
        )
    else:
        raise Exception("illegal component type "+component_type +
                        ". Allowed values: "+','.join(COMPONENT_TYPE_TO_MODULE.keys()))
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    dev.add_component(component_config)

    log.MainLogger().debug('openWB Version: ' + str(version))

    dev.update_values()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception:
        log.MainLogger().exception("Fehler im Modul openwb")
