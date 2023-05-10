#!/usr/bin/env python3
import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, IndependentComponentUpdater
from modules.common.req import get_http_session
from modules.devices.smart_me.counter import SmartMeCounter
from modules.devices.smart_me.config import (SmartMe, SmartMeConfiguration,
                                             SmartMeCounterConfiguration, SmartMeCounterSetup,
                                             SmartMeInverterConfiguration, SmartMeInverterSetup)
from modules.devices.smart_me.inverter import SmartMeInverter
log = logging.getLogger(__name__)


def create_device(device_config: SmartMe):
    def create_counter_component(component_config: SmartMeCounterSetup):
        return SmartMeCounter(component_config)

    def create_inverter_component(component_config: SmartMeInverterSetup):
        return SmartMeInverter(component_config)

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


def read_legacy(component_type: str, user: str, password: str, id_address: str) -> None:
    device = create_device(SmartMe(configuration=SmartMeConfiguration(user=user, password=password)))
    id = id_address[37:]
    if component_type == "counter":
        device.add_component(SmartMeCounterSetup(id=None, configuration=SmartMeCounterConfiguration(id=id)))
    else:
        device.add_component(SmartMeInverterSetup(id=1, configuration=SmartMeInverterConfiguration(id=id)))
    log.debug('Smartfox user: ' + user + ", password: " + password + ", id: " + id_address)
    device.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SmartMe)
