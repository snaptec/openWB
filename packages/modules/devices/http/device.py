#!/usr/bin/env python3
import logging
import re
from typing import Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common import req
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, IndependentComponentUpdater
from modules.devices.http.bat import HttpBat
from modules.devices.http.config import HTTP, HTTPConfiguration, HttpBatSetup, HttpCounterSetup, HttpInverterSetup, \
    HttpBatConfiguration, HttpCounterConfiguration, HttpInverterConfiguration
from modules.devices.http.counter import HttpCounter
from modules.devices.http.inverter import HttpInverter

log = logging.getLogger(__name__)


def create_device(device_config: HTTP):
    def create_bat_component(component_config: HttpBatSetup):
        return HttpBat(device_config.id, component_config, device_config.configuration.url)

    def create_counter_component(component_config: HttpCounterSetup):
        return HttpCounter(device_config.id, component_config, device_config.configuration.url)

    def create_inverter_component(component_config: HttpInverterSetup):
        return HttpInverter(device_config.id, component_config, device_config.configuration.url)

    session = req.get_http_session()
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=IndependentComponentUpdater(lambda component: component.update(session))
    )


def create_paths_dict(**kwargs):
    regex = re.compile("^(https?://[^/]+)(.*)")
    result = {}
    host_scheme = None
    for key, path in kwargs.items():
        if path != "none" and path != "":
            match = regex.search(path)
            if match is None:
                raise Exception("Invalid URL <" + path + ">: Absolute HTTP or HTTPS URL required")
            if host_scheme is None:
                host_scheme = match.group(1)
            elif host_scheme != match.group(1):
                raise Exception("All URLs must have the same scheme and host. However URLs are: " + str(kwargs))
            result[key] = match.group(2)
    return result


def run_device_legacy(device_config: HTTP, component_config: Union[HttpBatSetup, HttpCounterSetup, HttpInverterSetup]):
    device = create_device(device_config)
    device.add_component(component_config)
    log.debug("HTTP Configuration: %s, Component Configuration: %s", device_config, component_config)
    device.update()


def create_legacy_device_config(url: str):
    regex = re.compile("^(https?://[^/]+)(.*)")
    match = regex.search(url)
    if match is None:
        raise Exception("Invalid URL <" + url + ">: Absolute HTTP or HTTPS URL required")
    host_scheme = match.group(1)
    device_config = HTTP(configuration=HTTPConfiguration(url=host_scheme))
    return device_config


def read_legacy_bat(power_path: str, imported_path: str, exported_path: str, soc_path: str) -> None:
    component_config = HttpBatSetup(configuration=HttpBatConfiguration(**create_paths_dict(
        power_path=power_path,
        imported_path=imported_path,
        exported_path=exported_path,
        soc_path=soc_path,
    )))
    run_device_legacy(create_legacy_device_config(power_path), component_config)


def read_legacy_counter(power_path: str, imported_path: str, exported_path: str, current_l1_path: str,
                        current_l2_path: str, current_l3_path: str):
    component_config = HttpCounterSetup(configuration=HttpCounterConfiguration(**create_paths_dict(
        power_path=power_path,
        imported_path=imported_path,
        exported_path=exported_path,
        current_l1_path=current_l1_path,
        current_l2_path=current_l2_path,
        current_l3_path=current_l3_path,
    )))
    run_device_legacy(create_legacy_device_config(power_path), component_config)


def read_legacy_inverter(power_path: str, exported_path: str, num: int):
    component_config = HttpInverterSetup(id=num, configuration=HttpInverterConfiguration(**create_paths_dict(
        power_path=power_path,
        exported_path=exported_path,
    )))
    run_device_legacy(create_legacy_device_config(power_path), component_config)


def main(argv: List[str]):
    run_using_positional_cli_args(
        {"bat": read_legacy_bat, "counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv
    )


device_descriptor = DeviceDescriptor(configuration_factory=HTTP)
