from typing import List, Union
import sys

from helpermodules import log
from modules.common.abstract_device import AbstractDevice
from modules.common.component_state import SingleComponentUpdateContext
import counter
import inverter


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
        "inverter": inverter.PvKit
    }
    _components = []  # type: List[Union[counter.EvuKit, inverter.PvKit]]

    def __init__(self, device_config: dict) -> None:
        self.device_config = device_config

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components.append(self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"], component_config))

    def get_values(self) -> None:
        log.MainLogger().debug("Start device reading" + str(self._components))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(component.component_info):
                    component.update()
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
        "inverter": inverter
    }
    component_type = argv[1]
    version = int(argv[2])
    try:
        num = int(argv[3])
    except IndexError:
        num = None

    device_config = get_default_config()
    dev = Device(device_config)

    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    dev.add_component(component_config)

    log.MainLogger().debug('openWB Version: ' + str(version))

    dev.get_values()


if __name__ == "__main__":
    try:
        read_legacy(sys.argv)
    except Exception:
        log.MainLogger().exception("Fehler im Modul openwb")
