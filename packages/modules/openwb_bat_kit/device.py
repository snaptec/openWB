import logging

from modules.common import modbus
from modules.openwb_bat_kit import bat
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.abstract_device import AbstractDevice
from helpermodules.cli import run_using_positional_cli_args
from typing import Dict, Optional, List

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "OpenWB Speicher-Kit",
        "type": "openwb_bat_kit",
        "id": 0,
        "configuration": {}
    }


class Device(AbstractDevice):
    def __init__(self, device_config: dict) -> None:
        self.device_config = device_config
        self.components = {}  # type: Dict[str, bat.BatKit]
        self.client = modbus.ModbusClient("192.168.193.19", 8899)

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type == "bat":
            self.components["component"+str(component_config["id"])] = bat.BatKit(
                self.device_config["id"], component_config, self.client)
        else:
            raise Exception(
                "illegal component type " + component_type)

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self.components[component].component_info):
                    self.components[component].update()
        else:
            log.warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str, version: int, num: Optional[int] = None, evu_version: Optional[int] = None):
    """ Ausführung des Moduls als Python-Skript
    """

    device_config = get_default_config()
    dev = Device(device_config)

    component_config = get_component_config(component_type, version, num)
    dev.add_component(component_config)
    log.debug('openWB Version: ' + str(version))

    if component_type == "evu_inverter" and evu_version:
        component_config = get_component_config("counter", evu_version, None)
        dev.add_component(component_config)
        log.debug('openWB EVU-Version: ' + str(evu_version))

    dev.update()


def get_component_config(component_type: str, version: int, num: Optional[int] = None) -> Dict:
    if component_type == "bat":
        component_config = bat.get_default_config()
    else:
        raise Exception("illegal component type " + component_type)
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    return component_config


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
