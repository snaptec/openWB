#!/usr/bin/env python3
import logging
import time
from typing import Dict, Union, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.devices.huawei import bat
from modules.devices.huawei import counter
from modules.devices.huawei import inverter
from modules.devices.huawei.config import Huawei, HuaweiBatSetup, HuaweiCounterSetup, HuaweiInverterSetup

log = logging.getLogger(__name__)


huawei_component_classes = Union[bat.HuaweiBat, counter.HuaweiCounter, inverter.HuaweiInverter]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.HuaweiBat,
        "counter": counter.HuaweiCounter,
        "inverter": inverter.HuaweiInverter
    }

    def __init__(self, device_config: Union[Dict, Huawei]) -> None:
        self.components = {}  # type: Dict[str, huawei_component_classes]
        try:
            self.device_config = dataclass_from_dict(Huawei, device_config)
            ip_address = self.device_config.configuration.ip_address
            self.client = modbus.ModbusTcpClient_(ip_address, 502)
            self.client.delegate.connect()
            time.sleep(7)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict,
                                                    HuaweiBatSetup,
                                                    HuaweiCounterSetup,
                                                    HuaweiInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+component_type] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id,
                component_config, self.client,
                self.device_config.configuration.modbus_id))
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


def read_legacy(ip_address: str, modbus_id: int, read_counter: str = "False", read_battery: str = "False") -> None:
    components_to_read = ["inverter"]
    if read_counter.lower() == "true":
        components_to_read.append("counter")
    if read_battery.lower() == "true":
        components_to_read.append("bat")
    log.debug("components to read: " + str(components_to_read))

    device_config = Huawei()
    device_config.configuration.ip_address = ip_address
    device_config.configuration.modbus_id = modbus_id
    dev = Device(device_config)
    for component_type in components_to_read:
        if component_type in COMPONENT_TYPE_TO_MODULE:
            component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
        else:
            raise Exception(
                "illegal component type " + component_type + ". Allowed values: " +
                ','.join(COMPONENT_TYPE_TO_MODULE.keys())
            )
        if component_type == "counter" or component_type == "bat":
            num = None
        else:
            num = 1
        component_config.id = num
        dev.add_component(component_config)

    log.debug('Huawei IP-Adresse: ' + ip_address)
    log.debug('Huawei Modbus-ID: ' + str(modbus_id))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Huawei)
