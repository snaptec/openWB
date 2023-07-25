#!/usr/bin/env python3
import logging
from typing import Iterable, Optional, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.devices.youless import inverter
from modules.devices.youless.config import Youless, YoulessConfiguration, YoulessInverterSetup
from modules.devices.youless.inverter import YoulessInverter

log = logging.getLogger(__name__)


def create_device(device_config: Youless):
    def create_inverter_component(component_config: YoulessInverterSetup):
        return YoulessInverter(component_config)

    def update_components(components: Iterable[YoulessInverter]):
        response = req.get_http_session().get("http://"+device_config.configuration.ip_address+'/a',
                                              params=(('f', 'j'),),
                                              timeout=5).json()
        for component in components:
            component.update(response)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


COMPONENT_TYPE_TO_MODULE = {
    "inverter": inverter
}


def read_legacy(component_type: str, ip_address: str, source_s0: int, num: Optional[int]) -> None:
    device_config = Youless(configuration=YoulessConfiguration(ip_address=ip_address))
    dev = create_device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    component_config.configuration.source_s0 = True if source_s0 == 0 else False
    dev.add_component(component_config)

    log.debug('Youless IP-Adresse: ' + ip_address)
    log.debug('Youless source_s0: ' + str(source_s0))

    dev.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Youless)
