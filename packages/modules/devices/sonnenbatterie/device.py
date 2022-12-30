#!/usr/bin/env python3
""" Modul zum Auslesen von sonnenBatterie Speichern.
"""
import logging
from typing import Dict, Union, Optional, List

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.devices.sonnenbatterie import bat, counter, inverter
from modules.devices.sonnenbatterie.config import (SonnenBatterie, SonnenbatterieBatSetup, SonnenbatterieCounterSetup,
                                                   SonnenbatterieInverterSetup)
log = logging.getLogger(__name__)


sonnenbatterie_component_classes = Union[
    bat.SonnenbatterieBat,
    counter.SonnenbatterieCounter,
    inverter.SonnenbatterieInverter
]


class Device(AbstractDevice):
    COMPONENT_TYPE_TO_CLASS = {
        "bat": bat.SonnenbatterieBat,
        "counter": counter.SonnenbatterieCounter,
        "inverter": inverter.SonnenbatterieInverter
    }

    def __init__(self, device_config: Union[Dict, SonnenBatterie]) -> None:
        self.components = {}  # type: Dict[str, sonnenbatterie_component_classes]
        try:
            self.device_config = dataclass_from_dict(SonnenBatterie, device_config)
        except Exception:
            log.exception("Fehler im Modul "+self.device_config.name)

    def add_component(self, component_config: Union[Dict,
                                                    SonnenbatterieBatSetup,
                                                    SonnenbatterieCounterSetup,
                                                    SonnenbatterieInverterSetup]) -> None:
        if isinstance(component_config, Dict):
            component_type = component_config["type"]
        else:
            component_type = component_config.type
        component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
            component_type].component_descriptor.configuration_factory, component_config)
        if component_type in self.COMPONENT_TYPE_TO_CLASS:
            self.components["component"+str(component_config.id)] = (self.COMPONENT_TYPE_TO_CLASS[component_type](
                self.device_config.id,
                self.device_config.configuration.ip_address,
                self.device_config.configuration.variant,
                component_config))
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


def read_legacy(component_type: str, address: str, variant: int, num: Optional[int] = None) -> None:
    device_config = SonnenBatterie()
    device_config.configuration.ip_address = address
    device_config.configuration.variant = variant
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
    log.debug('SonnenBatterie address: ' + address)
    log.debug('SonnenBatterie variant: ' + str(variant))
    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SonnenBatterie)
