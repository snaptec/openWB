#!/usr/bin/env python3
import logging
import socket
import time
from typing import List, Optional, Union

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import DeviceDescriptor
from modules.common.configurable_device import ConfigurableDevice, ComponentFactoryByType, MultiComponentUpdater
from modules.common.fault_state import FaultState
from modules.devices.sma_shm import counter
from modules.devices.sma_shm import inverter
from modules.devices.sma_shm.config import SmaHomeManagerCounterSetup, SmaHomeManagerInverterSetup, Speedwire, \
    SmaHomeManagerCounterConfiguration, SmaHomeManagerInverterConfiguration
from modules.devices.sma_shm.speedwire_listener import SpeedwireListener
from modules.devices.sma_shm.utils import SpeedwireComponent

log = logging.getLogger(__name__)
timeout_seconds = 5


def update_components(components_todo: List[SpeedwireComponent]):
    with SpeedwireListener(timeout_seconds) as speedwire:
        stop_time = time.time() + timeout_seconds
        try:
            for sma_data in speedwire:
                components_todo = [component for component in components_todo if not component.read_datagram(sma_data)]
                if not components_todo:
                    log.debug("All components updated")
                    return
                if time.time() > stop_time:
                    break
        except socket.timeout:
            pass
        raise FaultState.error("Kein passendes Datagramm innerhalb des %ds timeout empfangen." % timeout_seconds)


def create_device(device_config: Speedwire):
    return ConfigurableDevice(
        device_config=device_config,
        component_factory=ComponentFactoryByType(counter=counter.create_component, inverter=inverter.create_component),
        component_updater=MultiComponentUpdater(update_components),
    )


def read_legacy(component_configuration: Union[SmaHomeManagerCounterSetup, SmaHomeManagerInverterSetup]):
    device = create_device(Speedwire())
    device.add_component(component_configuration)
    device.update()


def parse_serial(str: str) -> Optional[int]:
    return int(str) if str.isnumeric() else None


def read_legacy_counter(serial: str):
    read_legacy(SmaHomeManagerCounterSetup(configuration=SmaHomeManagerCounterConfiguration(parse_serial(serial))))


def read_legacy_inverter(serial: str, num: int):
    read_legacy(SmaHomeManagerInverterSetup(
        id=num, configuration=SmaHomeManagerInverterConfiguration(parse_serial(serial))
    ))


def main(argv: List[str]):
    run_using_positional_cli_args({"counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Speedwire)
