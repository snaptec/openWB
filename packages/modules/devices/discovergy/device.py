import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, IndependentComponentUpdater
from modules.common.req import get_http_session
from modules.devices.discovergy import counter, inverter
from modules.devices.discovergy.config import (
    Discovergy,
    DiscovergyConfiguration,
    DiscovergyCounterConfiguration,
    DiscovergyCounterSetup,
    DiscovergyInverterConfiguration,
    DiscovergyInverterSetup)

log = logging.getLogger(__name__)


def create_device(device_config: DiscovergyConfiguration):
    session = get_http_session()
    session.auth = (device_config.user, device_config.password)
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(counter=counter.create_component, inverter=inverter.create_component),
        component_updater=IndependentComponentUpdater(lambda component: component.update(session)),
    )


def read_legacy(user: str, password: str, meter_id_counter: str, meter_id_inverter: str):
    log.debug("Beginning update")
    device = create_device(DiscovergyConfiguration(user=user, password=password))
    if meter_id_counter:
        device.add_component(DiscovergyCounterSetup(
            id=None, configuration=DiscovergyCounterConfiguration(meter_id=meter_id_counter)
        ))
    if meter_id_inverter:
        device.add_component(DiscovergyInverterSetup(
            id=1, configuration=DiscovergyInverterConfiguration(meter_id=meter_id_inverter)
        ))
    device.update()
    log.debug("Update completed")


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Discovergy)
