import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import modbus
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, IndependentComponentUpdater
from modules.devices.kostal_sem.counter import KostalSemCounter
from modules.devices.kostal_sem.config import KostalSem, KostalSemConfiguration, KostalSemCounterSetup

log = logging.getLogger(__name__)


def create_device(device_config: KostalSemConfiguration):
    def create_counter_component(component_config: KostalSemCounterSetup):
        return KostalSemCounter(component_config, client)

    ip_address = device_config.ip_address
    client = modbus.ModbusTcpClient_(ip_address, 502)
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(counter=create_counter_component),
        component_updater=IndependentComponentUpdater(lambda component: component.update()),
    )


def read_legacy(address: str) -> None:
    device = create_device(KostalSemConfiguration(ip_address=address))
    device.add_component(KostalSemCounterSetup(id=None))
    log.debug('KSEM address: ' + address)
    device.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=KostalSem)
