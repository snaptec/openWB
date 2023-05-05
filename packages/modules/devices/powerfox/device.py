#!/usr/bin/env python3
import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, IndependentComponentUpdater
from modules.common.req import get_http_session
from modules.devices.powerfox.counter import PowerfoxCounter
from modules.devices.powerfox.config import (Powerfox, PowerfoxConfiguration,
                                             PowerfoxCounterConfiguration, PowerfoxCounterSetup,
                                             PowerfoxInverterConfiguration, PowerfoxInverterSetup)
from modules.devices.powerfox.inverter import PowerfoxInverter
log = logging.getLogger(__name__)


def create_device(device_config: Powerfox):
    def create_counter_component(component_config: PowerfoxCounterSetup):
        return PowerfoxCounter(component_config)

    def create_inverter_component(component_config: PowerfoxInverterSetup):
        return PowerfoxInverter(component_config)

    session = get_http_session()
    session.auth = (device_config.configuration.user, device_config.configuration.password)
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=IndependentComponentUpdater(lambda component: component.update(session))
    )


def read_legacy(component_type: str, user: str, password: str, id: str) -> None:
    device = create_device(Powerfox(configuration=PowerfoxConfiguration(user=user, password=password)))
    if component_type == "counter":
        device.add_component(PowerfoxCounterSetup(id=None, configuration=PowerfoxCounterConfiguration(id=id)))
    else:
        device.add_component(PowerfoxInverterSetup(id=1, configuration=PowerfoxInverterConfiguration(id=id)))
    log.debug('Smartfox user: ' + user + ", password: " + password + ", id: " + id)
    device.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Powerfox)
