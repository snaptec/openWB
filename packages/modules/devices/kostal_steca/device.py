#!/usr/bin/env python3
import logging
from typing import Optional, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import InverterState
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, IndependentComponentUpdater
from modules.devices.kostal_steca import inverter
from modules.devices.kostal_steca.config import KostalSteca, KostalStecaInverterSetup
from modules.devices.kostal_steca.inverter import KostalStecaInverter

log = logging.getLogger(__name__)


def create_device(device_config: KostalSteca):
    def create_inverter_component(component_config: KostalStecaInverterSetup):
        return KostalStecaInverter(component_config, device_config.configuration.ip_address)

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


def read_legacy(component_type: str, ip_address: str, variant: int, num: Optional[int]) -> None:
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    component_config.configuration.variant_steca = True if variant == 0 else False
    inverter = KostalStecaInverter(component_config, ip_address)

    log.debug('KostalSteca IP-Adresse: ' + ip_address)
    log.debug('KostalSteca Variant: ' + str(variant))

    with SingleComponentUpdateContext(inverter.component_info):
        power, exported = inverter.get_values()
        if exported is None:
            log.debug("PVkWh: NaN get prev. Value")
            with open("/var/www/html/openWB/ramdisk/pv2kwh", "r") as f:
                exported = f.read()

        inverter.store.set(InverterState(power=power, exported=exported))


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=KostalSteca)
