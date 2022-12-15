#!/usr/bin/env python3
import logging
from typing import List, Optional

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, IndependentComponentUpdater
from modules.devices.solar_view.counter import SolarViewCounter
from modules.devices.solar_view.config import (SolarView, SolarViewConfiguration,
                                               SolarViewCounterSetup,
                                               SolarViewInverterConfiguration, SolarViewInverterSetup)
from modules.devices.solar_view.inverter import SolarViewInverter
log = logging.getLogger(__name__)


def create_device(device_config: SolarView):
    def create_counter_component(component_config: SolarViewCounterSetup):
        return SolarViewCounter(component_config)

    def create_inverter_component(component_config: SolarViewInverterSetup):
        return SolarViewInverter(component_config)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=IndependentComponentUpdater(lambda component: component.update(
            device_config.configuration.ip_address,
            device_config.configuration.port,
            device_config.configuration.timeout))
    )


def read_legacy(component_type: str, ip_address: str, port: int, timeout: int, command: Optional[str] = None) -> None:
    device = create_device(SolarView(configuration=SolarViewConfiguration(
        ip_address=ip_address, port=port, timeout=timeout)))
    if component_type == "counter":
        device.add_component(SolarViewCounterSetup(id=None))
    else:
        device.add_component(SolarViewInverterSetup(
            id=1, configuration=SolarViewInverterConfiguration(command=command)))
    log.debug('SolarView ip_address: ' + ip_address + ", port: " +
              str(port) + ", timeout: " + str(timeout) + ", command: " + str(command))
    device.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SolarView)
