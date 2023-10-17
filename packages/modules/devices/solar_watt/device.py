#!/usr/bin/env python3
import logging
from typing import Dict, Iterable, List, Optional, Union

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ComponentFactoryByType, ConfigurableDevice, MultiComponentUpdater
from modules.common import req
from modules.devices.solar_watt.bat import SolarWattBat
from modules.devices.solar_watt.counter import SolarWattCounter
from modules.devices.solar_watt.config import (SolarWatt, SolarWattBatSetup, SolarWattConfiguration,
                                               SolarWattCounterSetup, SolarWattInverterSetup)
from modules.devices.solar_watt.inverter import SolarWattInverter

log = logging.getLogger(__name__)


def update(components: Iterable[Union[SolarWattBat, SolarWattCounter, SolarWattInverter]],
           energy_manager: bool,
           ip_adress: Optional[str] = None
           ):
    def request(url: str) -> Dict:
        response = req.get_http_session().get(url, timeout=3).json()
        if len(str(response)) < 10:
            raise ValueError("Antwort ungültig")
        return response

    energy_manager_response = None
    if energy_manager:
        energy_manager_response = request('http://'+ip_adress + '/rest/kiwigrid/wizard/devices')
    else:
        gateway_response = request('http://'+ip_adress+':8080/')
    for component in components:
        if isinstance(component, SolarWattInverter):
            if energy_manager_response is None:
                energy_manager_response = request('http://'+ip_adress + '/rest/kiwigrid/wizard/devices')
            component.update(energy_manager_response)
        else:
            if energy_manager:
                component.update(energy_manager_response, energy_manager)
            else:
                component.update(gateway_response, energy_manager)


def create_device(device_config: SolarWatt):
    def create_bat_component(component_config: SolarWattBatSetup):
        return SolarWattBat(device_config.id, component_config)

    def create_counter_component(component_config: SolarWattCounterSetup):
        return SolarWattCounter(device_config.id, component_config)

    def create_inverter_component(component_config: SolarWattInverterSetup):
        return SolarWattInverter(device_config.id, component_config)

    def update_components(components: Dict[str, Union[SolarWattBat, SolarWattCounter, SolarWattInverter]]):
        update(components, device_config.configuration.energy_manager, device_config.configuration.ip_adress)

    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat=create_bat_component,
            counter=create_counter_component,
            inverter=create_inverter_component,
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


def read_legacy(component_type: str,
                ip_address: str,
                ip2_address: Optional[str] = None,
                gateway: Optional[int] = None) -> None:
    if gateway is not None:
        if gateway == 0:
            energy_manager = True
        else:
            energy_manager = False
    else:
        energy_manager = False

    if component_type == "bat" or component_type == "counter":
        if energy_manager:
            ip = ip_address
        else:
            ip = ip2_address
        device = create_device(SolarWatt(configuration=SolarWattConfiguration(
            ip_address=ip, energy_manager=bool(energy_manager))))
        if component_type == "bat":
            device.add_component(SolarWattBatSetup(id=None))
        else:
            device.add_component(SolarWattCounterSetup(id=None))
    else:
        device = create_device(SolarWatt(configuration=SolarWattConfiguration(
            ip_address=ip_address, energy_manager=bool(energy_manager))))
        device.add_component(SolarWattInverterSetup(id=1))
    log.debug('SolarWatt ip_address: ' + ip_address + ', ip2_address: ' +
              str(ip2_address) + ", gateway: " + str(gateway))
    device.update()


def main(argv: List[str]):
    run_using_positional_cli_args(read_legacy, argv)


device_descriptor = DeviceDescriptor(configuration_factory=SolarWatt)
