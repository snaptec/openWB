from typing import Dict, Union, Optional, List

from helpermodules import log
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.openwb import bat
from modules.openwb import counter
from modules.openwb import inverter


def get_default_config() -> dict:
    return {
        "name": "OpenWB-Kit",
        "type": "openwb",
        "id": 0,
        "configuration": {}
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.BatKit,
        "counter": counter.EvuKit,
        "inverter": inverter.PvKit
    }

    def __init__(self, device_config: dict) -> None:
        self.device_config = device_config
        self._components = {}  # type: Dict[str, Union[counter.EvuKit, inverter.PvKit]]

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["id"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"], component_config))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.MainLogger().debug("Start device reading " + str(self._components))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self._components[component].component_info):
                    self._components[component].update()
        else:
            log.MainLogger().warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, version: int, num: Optional[int] = None):
    """ Ausführung des Moduls als Python-Skript
    """
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
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

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
