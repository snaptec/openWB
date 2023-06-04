#!/usr/bin/env python3
import logging
from typing import Dict, List, Union, Optional

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.devices.good_we import bat
from modules.devices.good_we import counter
from modules.devices.good_we import inverter
from modules.devices.good_we.config import (GoodWe, GoodWeBatSetup, GoodWeConfiguration, GoodWeCounterSetup,
                                            GoodWeInverterSetup)

log = logging.getLogger(__name__)

good_we_component_classes = Union[bat.GoodWeBat, counter.GoodWeCounter, inverter.GoodWeInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.GoodWeBat,
        "counter": counter.GoodWeCounter,
        "inverter": inverter.GoodWeInverter
    }

    def __init__(self, device_config: Union[Dict, GoodWe]) -> None:
        self.components = {}  # type: Dict[str, good_we_component_classes]
        try:
            self.device_config = dataclass_from_dict(GoodWe, device_config)
            ip_address = self.device_config.configuration.ip_address
            self.client = modbus.ModbusTcpClient_(ip_address, 502)
        except Exception:
            log.exception("Fehler im Modul " + self.device_config.name)

    def add_component(self,
                      component_config: Union[Dict, GoodWeBatSetup, GoodWeCounterSetup, GoodWeInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
                                                   component_type].component_descriptor.configuration_factory,
                                               component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component" + str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.configuration.modbus_id, component_config, self.client))
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
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str, ip_address: str, id: int, num: Optional[int]) -> None:
    device_config = GoodWe(configuration=GoodWeConfiguration(ip_address=ip_address, modbus_id=id))
    dev = Device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    dev.add_component(component_config)

    log.debug('GoodWe IP-Adresse: ' + ip_address)
    log.debug('GoodWe ID: ' + str(id))

    dev.update()
    dev.client.close_connection()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=GoodWe)
