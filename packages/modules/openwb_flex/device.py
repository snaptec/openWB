from typing import Any, Callable, List
import sys

try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_device import AbstractDevice, DeviceUpdater
    from ..common.abstract_component import ComponentUpdater
    from . import counter
except (ImportError, ValueError, SystemError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.abstract_device import AbstractDevice, DeviceUpdater
    from modules.common.abstract_component import ComponentUpdater
    import counter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit flex",
        "type": "openwb_flex",
        "id": 0,
        "configuration":
        {
            "ip_address": "192.168.193.15",
            "port": "8899"
        }
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        # "bat": ,
        "counter": counter.EvuKitFlex,
        # "inverter": inverter.PvKitFlex
    }
    _components = []  # type: List[ComponentUpdater]

    def __init__(self, device_config: dict) -> None:
        try:
            self.device_config = device_config
            ip_address = device_config["configuration"]["ip_address"]
            port = device_config["configuration"]["port"]
            self.client = modbus.ModbusClient(ip_address, port)
        except Exception:
            log.MainLogger().exception("Fehler im Modul " +
                                       device_config["name"])

    def add_component(self, factory: Callable[[dict, dict, Any],
                                              ComponentUpdater],
                      component_config: dict):
        self._components.append(
            factory(self.device_config, component_config, self.client))

    def get_values(self):
        log.MainLogger().debug("Start device reading" + str(self._components))
        if self._components:
            for component in self._components:
                state = component.get_values()
                log.MainLogger().debug("state " + str(state))
                component.set_values(state)
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(argv: List[str]):
    """ Ausführung des Moduls als Python-Skript
    """
    COMPONENT_TYPE_TO_MODULE = {
        # "bat": ,
        "counter": counter,
        # "inverter": inverter
    }
    log.MainLogger().debug('Start reading flex')
    component_type = argv[1]
    version = int(argv[2])
    ip_address = argv[3]
    port = int(argv[4])
    id = int(argv[5])
    try:
        num = int(argv[6])
    except IndexError:
        num = None

    device_config = get_default_config()
    device_config["configuration"]["ip_address"] = ip_address
    device_config["configuration"]["port"] = port
    dev = DeviceUpdater(Device(device_config))
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[
            component_type].get_default_config()
        module = COMPONENT_TYPE_TO_MODULE[component_type]
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))

    component_config["id"] = num
    component_config["configuration"]["version"] = version
    component_config["configuration"]["id"] = id
    dev.device.add_component(module.create_component, component_config)

    log.MainLogger().debug('openWB flex Version: ' + str(version))
    log.MainLogger().debug('openWB flex-Kit IP-Adresse: ' + str(ip_address))
    log.MainLogger().debug('openWB flex-Kit Port: ' + str(port))
    log.MainLogger().debug('openWB flex-Kit ID: ' + str(id))

    dev.get_values()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception:
        log.MainLogger().exception("Fehler im Modul openwb_flex")
