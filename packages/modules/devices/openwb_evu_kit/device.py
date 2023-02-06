import logging
import time
from typing import Dict, Union, Optional, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.devices.openwb_bat_kit.bat import BatKit
from modules.devices.openwb_evu_kit import bat
from modules.devices.openwb_evu_kit import counter
from modules.devices.openwb_evu_kit import inverter
from modules.devices.openwb_evu_kit.config import EvuKit, EvuKitBatSetup, EvuKitCounterSetup, EvuKitInverterSetup
from modules.devices.openwb_pv_kit.inverter import PvKit

log = logging.getLogger(__name__)


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": BatKit,
        "counter": counter.EvuKit,
        "inverter": PvKit
    }

    def __init__(self, device_config: Union[Dict, EvuKit]) -> None:
        self.device_config = dataclass_from_dict(EvuKit, device_config)
        self.components = {}  # type: Dict[str, Union[BatKit, counter.EvuKit, PvKit]]
        self.client = modbus.ModbusTcpClient_("192.168.193.15", 8899)

    def add_component(self,
                      component_config: Union[Dict, EvuKitBatSetup, EvuKitCounterSetup, EvuKitInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, component_config, self.client))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self.components[component].component_info):
                    self.components[component].update()
                    time.sleep(0.2)
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str,
                evu_version: int,
                bat_module: Optional[str] = "",
                bat_version: Optional[int] = 0,
                num: Optional[int] = None,
                inverter_module: Optional[str] = "",
                inverter_version: Optional[int] = 0):
    """ Ausführung des Moduls als Python-Skript
    """
    dev = Device(EvuKit())

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
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception("illegal component type " + component_type +
                        ". Allowed values: " +
                        ','.join(COMPONENT_TYPE_TO_MODULE.keys()))
    component_config.id = num
    component_config.configuration.version = version
    return component_config


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=EvuKit)
