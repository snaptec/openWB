#!/usr/bin/env python3
import logging
from typing import Iterable, Optional, Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import MultiComponentUpdateContext
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, MultiComponentUpdater
from modules.common.store import get_inverter_value_store
from modules.devices.batterx import bat, external_inverter
from modules.devices.batterx import counter
from modules.devices.batterx import inverter
from modules.devices.batterx.config import (BatterX, BatterXBatSetup, BatterXCounterSetup,
                                            BatterXExternalInverterSetup, BatterXInverterSetup)
from modules.common import req

log = logging.getLogger(__name__)


batterx_component_classes = Union[bat.BatterXBat, counter.BatterXCounter,
                                  inverter.BatterXInverter, external_inverter.BatterXExternalInverter]


def create_device(device_config: BatterX):
    def create_bat_component(component_config: BatterXBatSetup):
        return bat.BatterXBat(device_config.id, component_config)

    def create_counter_component(component_config: BatterXCounterSetup):
        return counter.BatterXCounter(device_config.id, component_config)

    def create_inverter_component(component_config: BatterXInverterSetup):
        return inverter.BatterXInverter(device_config.id, component_config)

    def create_external_inverter_component(component_config: BatterXExternalInverterSetup):
        return external_inverter.BatterXExternalInverter(device_config.id, component_config)

    def update_components(components: Iterable[batterx_component_classes]):
        resp_json = req.get_http_session().get(
                    'http://' + device_config.configuration.ip_address + '/api.php?get=currentstate',
                    timeout=5).json()
        for component in components:
            component.update(resp_json)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
            external_inverter=create_external_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


COMPONENT_TYPE_TO_MODULE = {
    "bat": bat,
    "counter": counter,
    "inverter": inverter,
    "external_inverter": external_inverter
}


def read_legacy(
        component_type: str,
        ip_address: str,
        num: Optional[int] = None,
        evu_counter: Optional[str] = None,
        bat_module: Optional[str] = None,
        ext_inverter: int = 0) -> None:

    device_config = BatterX()
    device_config.configuration.ip_address = ip_address
    dev = create_device(device_config)
    dev = _add_component(dev, component_type, num)
    if evu_counter == "bezug_batterx":
        dev = _add_component(dev, "counter", 0)
    if bat_module == "speicher_batterx":
        dev = _add_component(dev, "bat", 3)

    log.debug('BatterX IP-Adresse: ' + ip_address)
    log.debug('BatterX externer WR: ' + str(ext_inverter))

    with MultiComponentUpdateContext(dev.components):
        resp_json = req.get_http_session().get(
            'http://' + ip_address + '/api.php?get=currentstate',
            timeout=5).json()
        for component in dev.components.values():
            if isinstance(component, (bat.BatterXBat, counter.BatterXCounter)):
                component.update(resp_json)
            elif isinstance(component, inverter.BatterXInverter):
                if ext_inverter == 0:
                    component.update(resp_json)
                else:
                    dev = _add_component(dev, "external_inverter", 4)
                    power = component.get_power(resp_json)
                    power_ext = dev.components["component4"].get_power(resp_json)
                    state = component.get_inverter_state(power+power_ext)
                    get_inverter_value_store(num).set(state)


def _add_component(dev: ConfigurableDevice, component_type: str, num: Optional[int]) -> ConfigurableDevice:
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = num
    dev.add_component(component_config)
    return dev


def main(argv: List[str]) -> None:
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=BatterX)
