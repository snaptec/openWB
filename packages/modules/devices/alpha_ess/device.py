#!/usr/bin/env python3
import logging
from typing import Dict, Union, Optional, List

from modules.devices.alpha_ess.config import AlphaEss, AlphaEssBatSetup, AlphaEssCounterSetup, AlphaEssInverterSetup
from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.devices.alpha_ess import bat
from modules.devices.alpha_ess import counter
from modules.devices.alpha_ess import inverter

log = logging.getLogger(__name__)


alpha_ess_component_classes = Union[bat.AlphaEssBat, counter.AlphaEssCounter, inverter.AlphaEssInverter]
default_unit_id = 85


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.AlphaEssBat,
        "counter": counter.AlphaEssCounter,
        "inverter": inverter.AlphaEssInverter
    }

    def __init__(self, device_config: Union[Dict, AlphaEss]) -> None:
        self.components = {}  # type: Dict[str, alpha_ess_component_classes]
        try:
            self.device_config = dataclass_from_dict(AlphaEss, device_config)
            if self.device_config.configuration.source == 0:
                self.client = modbus.ModbusTcpClient_("192.168.193.125", 8899)
            else:
                self.client = modbus.ModbusTcpClient_(self.device_config.configuration.ip_address, 502)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self,
                      component_config: Union[Dict,
                                              AlphaEssBatSetup,
                                              AlphaEssCounterSetup,
                                              AlphaEssInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id,
                component_config,
                self.client,
                self.device_config.configuration))
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
                        self.components[component].update(unit_id=default_unit_id)
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


def read_legacy(component_type: str, source: int, version: int, ip_address: str, num: Optional[int] = None) -> None:
    device_config = AlphaEss()
    device_config.configuration.source = source
    device_config.configuration.version = version
    device_config.configuration.ip_address = ip_address
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

    log.debug('alpha_ess Version: ' + str(version))
    log.debug('alpha_ess IP-Adresse: ' + str(ip_address))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=AlphaEss)
