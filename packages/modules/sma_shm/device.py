#!/usr/bin/env python3
import logging
import socket
import time
from typing import Dict, List, Callable, Iterator, Optional, Union

from dataclass_utils import dataclass_from_dict
from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice, DeviceDescriptor
from modules.common.component_context import MultiComponentUpdateContext
from modules.common.fault_state import FaultState
from modules.sma_shm import counter
from modules.sma_shm import inverter
from modules.sma_shm.config import SmaHomeManagerCounterSetup, SmaHomeManagerInverterSetup, Speedwire
from modules.sma_shm.speedwire_listener import SpeedwireListener
from modules.sma_shm.utils import SpeedwireComponent


log = logging.getLogger(__name__)
timeout_seconds = 5


class Device(AbstractDevice):
    COMPONENT_FACTORIES = {
        "counter": counter.create_component,
        "inverter": inverter.create_component
    }

    def __init__(self, device_config: Union[Dict, Speedwire]) -> None:
        self.components = {}  # type: Dict[str, SpeedwireComponent]
        self.device_config = dataclass_from_dict(Speedwire, device_config)

    def add_component(self,
                      component_config: Union[Dict, SmaHomeManagerCounterSetup, SmaHomeManagerInverterSetup]) -> None:
        try:
            if isinstance(component_config, Dict):
                component_type = component_config["type"]
            else:
                component_type = component_config.type
            component_config = dataclass_from_dict(COMPONENT_TYPE_TO_MODULE[
                component_type].component_descriptor.configuration_factory, component_config)
            factory = self.COMPONENT_FACTORIES[component_config.type]
        except KeyError as e:
            raise Exception(
                "Unknown component type <%s>, known types are: <%s>", e, ','.join(self.COMPONENT_FACTORIES.keys())
            )
        self.components["component"+str(component_config.id)] = factory(component_config)

    def update(self) -> None:
        log.debug("Beginning update")
        with MultiComponentUpdateContext(self.components):
            if not self.components:
                raise FaultState.warning("Keine Komponenten konfiguriert")

            with SpeedwireListener(timeout_seconds) as speedwire:
                self.__read_speedwire(speedwire)

        log.debug("Update complete")

    def __read_speedwire(self, speedwire: Iterator[dict]):
        stop_time = time.time() + timeout_seconds
        components_todo = self.components.values()
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


COMPONENT_TYPE_TO_MODULE = {
    "counter": counter,
    "inverter": inverter
}


def read_legacy(configuration_factory: Callable[[],
                                                Union[SmaHomeManagerCounterSetup, SmaHomeManagerInverterSetup]],
                serial: str,
                num: Optional[int] = None):
    device = Device(Speedwire())
    component_config = configuration_factory()
    component_config.configuration.serials = int(serial) if serial.isnumeric() else None
    component_config.id = num
    device.add_component(component_config)
    device.update()


def read_legacy_counter(serial: str):
    read_legacy(counter.component_descriptor.configuration_factory, serial)


def read_legacy_inverter(serial: str, num: int):
    read_legacy(inverter.component_descriptor.configuration_factory, serial, num)


def main(argv: List[str]):
    run_using_positional_cli_args({"counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv)


device_descriptor = DeviceDescriptor(configuration_factory=Speedwire)
