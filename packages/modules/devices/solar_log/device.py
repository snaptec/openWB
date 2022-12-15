#!/usr/bin/env python3
import json
import logging
from typing import List, Union

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, MultiComponentUpdater
from modules.common import req
from modules.devices.solar_log.counter import SolarLogCounter
from modules.devices.solar_log.config import (SolarLog, SolarLogConfiguration,
                                              SolarLogCounterSetup,
                                              SolarLogInverterSetup)
from modules.devices.solar_log.inverter import SolarLogInverter
log = logging.getLogger(__name__)


def create_device(device_config: SolarLogConfiguration):
    def create_counter_component(component_config: SolarLogCounterSetup):
        return SolarLogCounter(component_config)

    def create_inverter_component(component_config: SolarLogInverterSetup):
        return SolarLogInverter(component_config)

    def update_components(components: Union[SolarLogCounter, SolarLogInverter]):
        response = req.get_http_session().post('http://'+device_config.ip_adress+'/getjp',
                                               data=json.dumps({"801": {"170": None}}), timeout=5).json()
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


def read_legacy(component_type: str, ip_address: str, password: str, id: str) -> None:
    device = create_device(SolarLogConfiguration(ip_address=ip_address))
    if component_type == "counter":
        device.add_component(SolarLogCounterSetup(id=None))
    else:
        device.add_component(SolarLogInverterSetup(id=1))
    log.debug('Solar-Log ip_address: ' + ip_address)
    device.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SolarLog)
