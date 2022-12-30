#!/usr/bin/env python3
import logging
from typing import List, Union, Iterable

from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.devices.json import bat, counter, inverter
from modules.devices.json.bat import JsonBat
from modules.devices.json.config import (Json,
                                         JsonBatConfiguration,
                                         JsonBatSetup,
                                         JsonConfiguration,
                                         JsonCounterConfiguration,
                                         JsonCounterSetup,
                                         JsonInverterConfiguration,
                                         JsonInverterSetup)
from modules.devices.json.counter import JsonCounter
from modules.devices.json.inverter import JsonInverter

log = logging.getLogger(__name__)
JsonComponent = Union[JsonBat, JsonCounter, JsonInverter]


def create_device(device_config: Json):
    def create_bat(component_config: JsonBatSetup) -> JsonBat:
        return JsonBat(device_config.id, component_config)

    def create_counter(component_config: JsonCounterSetup) -> JsonCounter:
        return JsonCounter(device_config.id, component_config)

    def create_inverter(component_config: JsonInverterSetup) -> JsonInverter:
        return JsonInverter(device_config.id, component_config)

    def update_components(components: Iterable[JsonComponent]):
        response = req.get_http_session().get(device_config.configuration.url, timeout=5).json()
        for component in components:
            component.update(response)

    return ConfigurableDevice(
        device_config,
        component_factory=ComponentFactoryByType(bat=create_bat, counter=create_counter, inverter=create_inverter),
        component_updater=MultiComponentUpdater(update_components)
    )


def read_legacy(url: str, component_config: Union[JsonBatSetup, JsonCounterSetup, JsonInverterSetup]) -> None:
    dev = create_device(Json(configuration=JsonConfiguration(url=url)))
    dev.add_component(component_config)
    dev.update()


def read_legacy_bat(ip_address: str, jq_power: str, jq_soc: str):
    config = JsonBatConfiguration(jq_power=jq_power, jq_soc=jq_soc)
    read_legacy(ip_address, bat.component_descriptor.configuration_factory(id=None, configuration=config))


def read_legacy_counter(ip_address: str, jq_power: str, jq_imported: str, jq_exported: str):
    config = JsonCounterConfiguration(jq_power=jq_power,
                                      jq_imported=None if jq_imported == "" else jq_imported,
                                      jq_exported=None if jq_exported == "" else jq_exported)
    read_legacy(
        ip_address,
        counter.component_descriptor.configuration_factory(id=None, configuration=config))


def read_legacy_inverter(ip_address: str, jq_power: str, jq_exported: str, num: int):
    config = JsonInverterConfiguration(jq_power=jq_power, jq_exported=None if jq_exported == "" else jq_exported)
    read_legacy(ip_address, inverter.component_descriptor.configuration_factory(id=num, configuration=config))


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )


device_descriptor = DeviceDescriptor(configuration_factory=Json)
