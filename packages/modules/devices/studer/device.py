#!/usr/bin/env python3
""" Modul zum Auslesen von Alpha Ess Speichern, Zählern und Wechselrichtern.
"""
import logging
from typing import Dict, List, Union, Optional

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.devices.studer import bat
from modules.devices.studer import inverter
from modules.devices.studer.config import Studer, StuderBatSetup, StuderInverterConfiguration, StuderInverterSetup

log = logging.getLogger(__name__)


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.StuderBat,
        "inverter": inverter.StuderInverter
    }

    def __init__(self, device_config: Union[Dict, Studer]) -> None:
        self.components = {}  # type: Dict[str, Union[bat.StuderBat, inverter.StuderInverter]]
        try:
            self.device_config = dataclass_from_dict(Studer, device_config)
            ip_address = self.device_config.configuration.ip_address
            self.client = modbus.ModbusTcpClient_(ip_address, 502)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict, StuderBatSetup, StuderInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                component_config, self.client))
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
        else:
            log.warning(
                self.device_config.name +
                ": Es konnten keine Werte gelesen werden, da noch keine Komponenten konfiguriert wurden."
            )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "inverter": inverter
}


def read_legacy(ip_address: str, component_config: Union[StuderBatSetup, StuderInverterSetup]):
    device_config = Studer()
    device_config.configuration.ip_address = ip_address
    dev = Device(device_config)
    dev.add_component(component_config)
    dev.update()


def read_legacy_bat(ip_address: str, num: Optional[int] = None):
    read_legacy(ip_address, bat.component_descriptor.configuration_factory(id=None))


def read_legacy_inverter(ip_address: str, vc_count: int, vc_type: str, num: int):
    read_legacy(ip_address, inverter.component_descriptor.configuration_factory(
        id=num, configuration=StuderInverterConfiguration(vc_count=vc_count, vc_type=vc_type)))


def main(argv: List[str]):
    run_using_positional_cli_args({"bat": read_legacy_bat, "inverter": read_legacy_inverter}, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Studer)
