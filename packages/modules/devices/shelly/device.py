#!/usr/bin/env python3
import logging
from typing import List
import os
from modules.common import req

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import (ConfigurableDevice, ComponentFactoryByType, IndependentComponentUpdater)
from modules.devices.shelly.inverter import ShellyInverter
from modules.devices.shelly.config import Shelly, ShellyConfiguration
from modules.devices.shelly.config import ShellyInverterSetup, ShellyInverterConfiguration


log = logging.getLogger(__name__)


def create_device(device_config: Shelly) -> ConfigurableDevice:
    def create_inverter_component(component_config: ShellyInverterSetup) -> ShellyInverter:
        return ShellyInverter(device_config.id, component_config, device_config.configuration.address,
                              device_config.configuration.generation)

    if device_config.configuration.generation is None and device_config.configuration.address is not None:
        device_config.configuration.generation = 1
        url = "http://" + device_config.configuration.address + "/shelly"
        answergen = req.get_http_session().get(url, timeout=3).json()
        if 'gen' in answergen:
            device_config.configuration.generation = int(answergen['gen'])

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            inverter=create_inverter_component
        ),
        component_updater=IndependentComponentUpdater(lambda component: component.update())
    )


def run_device_legacy(device_config: Shelly,
                      component_config: ShellyInverterSetup) -> None:
    device = create_device(device_config)
    device.add_component(component_config)
    log.debug("Shelly Configuration: %s, Component Configuration: %s", device_config, component_config)
    device.update()


def create_legacy_device_config(address: str, generation: int,
                                num: int) -> Shelly:
    device_config = Shelly(configuration=ShellyConfiguration(address=address, generation=generation), id=num)
    log.debug("Config: %s", device_config)
    return device_config


def read_legacy_inverter(address: str, num: int) -> None:
    component_config = ShellyInverterSetup(configuration=ShellyInverterConfiguration())
    component_config.id = num
    generation = 1
    fnameg = '/var/www/html/openWB/ramdisk/shelly_wr_ret.' + address + '_shelly_infog'
    if os.path.isfile(fnameg):
        with open(fnameg, 'r') as f:
            generation = int(f.read())
    else:
        url = "http://" + address + "/shelly"
        answergen = req.get_http_session().get(url, timeout=3).json()
        if 'gen' in answergen:
            generation = int(answergen['gen'])
        with open(fnameg, 'w') as f:
            f.write(str(generation))
    run_device_legacy(create_legacy_device_config(address, generation,
                                                  num), component_config)


def main(argv: List[str]) -> None:
    run_using_positional_cli_args(
        {"inverter": read_legacy_inverter}, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Shelly)
