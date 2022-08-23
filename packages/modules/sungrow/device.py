#!/usr/bin/env python3
import logging
from typing import Dict, List, Union, Optional

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.sungrow import bat
from modules.sungrow import counter
from modules.sungrow import inverter
from modules.sungrow.config import (Sungrow, SungrowBatSetup, SungrowCounterConfiguration, SungrowCounterSetup,
                                    SungrowInverterSetup)

log = logging.getLogger(__name__)


sungrow_component_classes = Union[bat.SungrowBat, counter.SungrowCounter, inverter.SungrowInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.SungrowBat,
        "counter": counter.SungrowCounter,
        "inverter": inverter.SungrowInverter
    }

    def __init__(self, device_config: Union[Dict, Sungrow]) -> None:
        self.components = {}  # type: Dict[str, sungrow_component_classes]
        try:
            self.device_config = dataclass_from_dict(Sungrow, device_config)
            self.client = modbus.ModbusTcpClient_(self.device_config.configuration.ip_address,
                                                  self.device_config.configuration.port)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self,
                      component_config: Union[Dict,
                                              SungrowBatSetup, SungrowCounterSetup, SungrowInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id, self.device_config.configuration.modbus_id, component_config, self.client))
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(self.COMPONENT_TYPE_TO_CLASS.keys())
            )

    def update(self) -> None:
        log.debug("Start device reading " + str(self.components))
        if self.components:
            with self.client:
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
    "counter": counter,
    "inverter": inverter
}


def read_legacy(ip_address: str, port: int, modbus_id: int, component_config: dict):
    device_config = Sungrow()
    device_config.configuration.ip_address = ip_address
    device_config.configuration.port = port
    device_config.configuration.modbus_id = modbus_id
    dev = Device(device_config)
    dev.add_component(component_config)
    dev.update()


def read_legacy_bat(ip_address: str, port, modbus_id: int, num: Optional[int] = None):
    read_legacy(ip_address, port, modbus_id, bat.component_descriptor.configuration_factory(id=None))


def read_legacy_counter(ip_address: str, port: int, modbus_id: int, version: int):
    read_legacy(ip_address, port, modbus_id, counter.component_descriptor.configuration_factory(
        id=None, configuration=SungrowCounterConfiguration(version=version)))


def read_legacy_inverter(ip_address: str, port: int, modbus_id: int, num: int):
    read_legacy(ip_address, port, modbus_id, inverter.component_descriptor.configuration_factory(id=num))


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )


device_descriptor = DeviceDescriptor(configuration_factory=Sungrow)
