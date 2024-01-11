#!/usr/bin/env python3
import logging
from typing import Iterable, Optional, Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.devices.solar_world import counter, inverter
from modules.devices.solar_world.config import (
    SolarWorld, SolarWorldConfiguration, SolarWorldCounterSetup, SolarWorldInverterSetup)
from modules.devices.solar_world.counter import SolarWorldCounter
from modules.devices.solar_world.inverter import SolarWorldInverter

log = logging.getLogger(__name__)


def create_device(device_config: SolarWorld):
    def create_counter_component(component_config: SolarWorldCounterSetup):
        return SolarWorldCounter(device_config.id, component_config)

    def create_inverter_component(component_config: SolarWorldInverterSetup):
        return SolarWorldInverter(device_config.id, component_config)

    def update_components(components: Iterable[Union[SolarWorldCounter, SolarWorldInverter]]):
        response = req.get_http_session().get("http://"+str(device_config.configuration.ip_address) +
                                              "/rest/solarworld/lpvm/powerAndBatteryData", timeout=5).json()
        for component in components:
            component.update(response)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


COMPONENT_TYPE_TO_MODULE = {
    "counter": counter,
    "inverter": inverter
}


def read_legacy(component_type: str, ip_address: str, num: Optional[int]) -> None:
    device_config = SolarWorld(configuration=SolarWorldConfiguration(ip_address=ip_address))
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

    log.debug('SolarWorld IP-Adresse: ' + ip_address)

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SolarWorld)
