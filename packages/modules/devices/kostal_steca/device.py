#!/usr/bin/env python3
import logging
from typing import Iterable, Optional, Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, IndependentComponentUpdater
from modules.devices.kostal_steca import inverter
from modules.devices.kostal_steca.config import KostalSteca, KostalStecaConfiguration, KostalStecaInverterSetup
from modules.devices.kostal_steca.inverter import KostalStecaInverter

log = logging.getLogger(__name__)


def create_device(device_config: KostalSteca):
    def create_inverter_component(component_config: KostalStecaInverterSetup):
        return KostalStecaInverter(device_config.id, component_config)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            inverter=create_inverter_component,
        ),
        component_updater=IndependentComponentUpdater(lambda component: component.update())
    )


COMPONENT_TYPE_TO_MODULE = {
    "inverter": inverter
}


def read_legacy(component_type: str, ip_address: str, id: int, num: Optional[int]) -> None:
    device_config = KostalSteca(configuration=KostalStecaConfiguration(ip_address=ip_address, id=id))
    dev = create_device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    dev.add_component(component_config)

    log.debug('KostalSteca IP-Adresse: ' + ip_address)
    log.debug('KostalSteca ID: ' + str(id))

    dev.update()
    # Hier kann es notwendig sein, für 1.9 eine eigene Update-Methode zu implemenitieren, die die Werte wie benötigt miteinander verrechnet.
    # Hier muss auch bei Hybrid-Systemen die Speicher-und PV-Leistung verrechnet werden.


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=KostalSteca)
