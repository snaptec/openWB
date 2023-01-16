#!/usr/bin/env python3
import logging
from typing import Iterable, Tuple, Union, List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.component_context import SingleComponentUpdateContext
from modules.common.component_state import BatState
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.common.modbus import ModbusTcpClient_
from modules.devices.varta import bat_api, counter
from modules.devices.varta import bat_modbus
from modules.devices.varta.bat_api import VartaBatApi
from modules.devices.varta.bat_modbus import VartaBatModbus
from modules.devices.varta.config import (Varta, VartaConfiguration, VartaBatApiSetup, VartaBatModbusSetup,
                                          VartaCounterSetup)
from modules.devices.varta.counter import VartaCounter

log = logging.getLogger(__name__)


def create_device(device_config: Varta):
    def create_bat_api_component(component_config: VartaBatApiSetup):
        return VartaBatApi(device_config.id, component_config, device_config.configuration.ip_address)

    def create_bat_modbus_component(component_config: VartaBatModbusSetup):
        return VartaBatModbus(device_config.id, component_config)

    def create_counter_component(component_config: VartaCounterSetup):
        return VartaCounter(device_config.id, component_config)

    def update_components(components: Iterable[Union[VartaBatApi, VartaBatModbus, VartaCounter]]):
        with client as c:
            for component in components:
                if isinstance(component, (VartaBatModbus, VartaCounter)):
                    with SingleComponentUpdateContext(component.component_info):
                        component.update(c)
        for component in components:
            if isinstance(component, (VartaBatApi)):
                with SingleComponentUpdateContext(component.component_info):
                    component.update()

    try:
        client = ModbusTcpClient_(device_config.configuration.ip_address, 502)
    except Exception:
        log.exception("Fehler in create_device")
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(
            bat_api=create_bat_api_component,
            bat_modbus=create_bat_modbus_component,
            counter=create_counter_component
        ),
        component_updater=MultiComponentUpdater(update_components)
    )


COMPONENT_TYPE_TO_MODULE = {
    "bat_api": bat_api,
    "bat_modbus": bat_modbus,
    "counter": counter
}


def create_device_with_components(component_type: str, ip_address: str):
    device_config = Varta(configuration=VartaConfiguration(ip_address=ip_address))
    dev = create_device(device_config)
    if component_type in COMPONENT_TYPE_TO_MODULE:
        component_config = COMPONENT_TYPE_TO_MODULE[component_type].component_descriptor.configuration_factory()
    else:
        raise Exception(
            "illegal component type " + component_type + ". Allowed values: " +
            ','.join(COMPONENT_TYPE_TO_MODULE.keys())
        )
    component_config.id = None
    dev.add_component(component_config)

    log.debug('Varta IP-Adresse: ' + ip_address)
    return dev


def update_counter(ip_address: str):
    create_device_with_components("counter", ip_address).update()


def update_bat_api(ip_address: str):
    create_device_with_components("bat_api", ip_address).update()


def create_modbus_bat(ip_address) -> Tuple[ModbusTcpClient_, VartaBatModbus]:
    client = ModbusTcpClient_(ip_address, 502)
    bat = VartaBatModbus(None, VartaBatModbusSetup())
    log.debug('Varta IP-Adresse: ' + ip_address)
    return client, bat


def get_modbus_bat_state(client: ModbusTcpClient_, bat: VartaBatModbus) -> BatState:
    with client as c:
        with SingleComponentUpdateContext(bat.component_info):
            return bat.get_state(c)


def update_two_batteries(ip_address: str, ip_address2: str) -> None:
    client1, bat1 = create_modbus_bat(ip_address)
    bat_state_1 = get_modbus_bat_state(client1, bat1)
    if ip_address2 != "none":
        client2, bat2 = create_modbus_bat(ip_address2)
        bat_state_2 = get_modbus_bat_state(client2, bat2)
        soc = (bat_state_1.soc + bat_state_2.soc)/2
        power = bat_state_1.power + bat_state_2.power
    else:
        soc = bat_state_1.soc
        power = bat_state_1.power

    bat1.set_state(BatState(soc=soc, power=power))


def main(argv: List[str]):
    run_using_positional_cli_args({"bat_api": update_bat_api,
                                  "bat_modbus": update_two_batteries, "counter": update_counter}, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Varta)
