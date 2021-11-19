from typing import Any, Callable, List
import sys

try:
    from ..common.abstract_device import AbstractDevice, DeviceUpdater
    from ..common.abstract_component import ComponentUpdater
    from ...helpermodules import log
    from . import counter
except (ImportError, ValueError, SystemError):
    from helpermodules import log
    from modules.common.abstract_device import AbstractDevice, DeviceUpdater
    from modules.common.abstract_component import ComponentUpdater
    import counter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit",
        "type": "openwb",
        "id": 0
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        # "bat": ,
        "counter": counter.EvuKit,
        # "inverter": inverter.PvKit
    }
    components = []  # type: List[ComponentUpdater]

    def __init__(self, device_config: dict) -> None:
        self.device_config = device_config

    def add_component(self, factory: Callable[[dict, dict, Any], ComponentUpdater], component_config: dict):
        self.components.append(factory(self.device_config, component_config, None))


def read_legacy(argv: List[str]):
    """ Ausführung des Moduls als Python-Skript
    """
    COMPONENT_TYPE_TO_MODULE = {
        # "bat": ,
        "counter": counter,
        # "inverter": inverter
    }
    component_type = argv[1]
    version = int(argv[2])
    try:
        num = int(argv[3])
    except IndexError:
        num = None

    device_config = get_default_config()
    dev = DeviceUpdater(Device(device_config))

    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
        module = COMPONENT_TYPE_TO_MODULE[component_type]
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    dev.device.add_component(module.create_component, component_config)

    log.MainLogger().debug('openWB Version: ' + str(version))

    dev.get_values()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception:
        log.MainLogger().exception("Fehler im Modul openwb")
