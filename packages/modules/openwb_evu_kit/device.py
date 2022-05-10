import logging
import time
from typing import Dict, Union, Optional, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import SingleComponentUpdateContext
from modules.openwb_evu_kit import bat
from modules.openwb_evu_kit import counter
from modules.openwb_evu_kit import inverter
from modules.openwb_bat_kit.bat import BatKit
from modules.openwb_pv_kit.inverter import PvKit
from modules.common import modbus

log = logging.getLogger(__name__)


def get_default_config() -> dict:
    return {
        "name": "OpenWB EVU-Kit",
        "type": "openwb_evu_kit",
        "id": 0,
        "configuration": {}
    }


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": BatKit,
        "counter": counter.EvuKit,
        "inverter": PvKit
    }

    def __init__(self, device_config: dict) -> None:
        self.device_config = device_config
        # type: Dict[str, Union[bat.BatKit, counter.EvuKit, inverter.PvKit]]
        self._components = {}
        self.client = modbus.ModbusClient("192.168.193.15", 8899)

    def add_component(self, component_config: dict) -> None:
        component_type = component_config["type"]
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self._components["component"+str(component_config["type"])] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config["id"], component_config, self.client))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self._components))
        if self._components:
            for component in self._components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self._components[component].component_info):
                    self._components[component].update()
                    time.sleep(0.2)
        else:
            log.warning(
                self.device_config["name"] +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


def read_legacy(component_type: str,
                evu_version: int,
                bat_module: Optional[str] = "",
                bat_version: Optional[int] = 0,
                num: Optional[int] = None,
                inverter_module: Optional[str] = "",
                inverter_version: Optional[int] = 0):
    """ Ausführung des Moduls als Python-Skript
    """

    device_config = get_default_config()
    dev = Device(device_config)

    component_config = get_component_config(component_type, evu_version, None)
    dev.add_component(component_config)
    log.debug('openWB Version: ' + str(evu_version))

    if inverter_module == "wr_ethmpm3pmaevu" or inverter_module == "wr2_ethlovatoaevu":
        component_config = get_component_config("inverter", inverter_version, num)
        dev.add_component(component_config)
        log.debug('openWB Inverter-Version: ' + str(inverter_version))
    if bat_module == "speicher_sdmaevu":
        component_config = get_component_config("bat", bat_version, None)
        dev.add_component(component_config)
        log.debug('openWB Bat-Version: ' + str(bat_version))

    dev.update()


def get_component_config(component_type: str, version: Optional[int], num: Optional[int] = None) -> Dict:
    COMPONENT_TYPE_TO_MODULE = {
        "bat": bat,
        "counter": counter,
        "inverter": inverter
    }
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].get_default_config()
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))
    component_config["id"] = num
    component_config["configuration"]["version"] = version
    return component_config


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)
