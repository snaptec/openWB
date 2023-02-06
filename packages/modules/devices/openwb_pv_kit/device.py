import logging
from typing import Dict, Optional, List, Union

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.devices.openwb_pv_kit import inverter
from modules.devices.openwb_pv_kit.config import PvKit, PvKitInverterSetup

log = logging.getLogger(__name__)


class Device(AbstractDevice):
    def __init__(self, device_config: Union[Dict, PvKit]) -> None:
        self.device_config = dataclass_from_dict(PvKit, device_config)
        self.components = {}  # type: Dict[str, inverter.PvKit]
        self.client = modbus.ModbusTcpClient_("192.168.193.13", 8899)

    def add_component(self, component_config: Union[Dict, PvKitInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type == "inverter":
            self.components["component"+str(component_config.id)] = inverter.PvKit(
                self.device_config.id, component_config, self.client)
        else:
            raise Exception("illegal component type " + component_type)

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            for component in self.components:
                # Auch wenn bei einer Komponente ein Fehler auftritt, sollen alle anderen noch ausgelesen werden.
                with SingleComponentUpdateContext(self.components[component].component_info):
                    self.components[component].update()
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "inverter": inverter
}


def read_legacy(component_type: str, version: int, num: Optional[int] = None, evu_version: Optional[int] = None):
    """ Ausführung des Moduls als Python-Skript
    """
    dev = Device(PvKit())

    component_config = get_component_config(component_type, version, num)
    dev.add_component(component_config)
    log.debug('openWB Version: ' + str(version))

    if component_type == "evu_inverter" and evu_version:
        component_config = get_component_config("counter", evu_version, None)
        dev.add_component(component_config)
        log.debug('openWB EVU-Version: ' + str(evu_version))

    dev.update()


def get_component_config(component_type: str, version: int, num: Optional[int] = None) -> Dict:
    if component_type == "inverter":
        component_config = inverter.component_descriptor.configuration_factory()
    else:
        raise Exception("illegal component type " + component_type)
    component_config.id = num
    component_config.configuration.version = version
    return component_config


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=PvKit)
