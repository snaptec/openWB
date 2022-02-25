#!/usr/bin/env python3
import logging
import socket
import time
from typing import List, Callable, Iterator

from helpermodules.cli import run_using_positional_cli_args
from modules.common.abstract_device import AbstractDevice
from modules.common.component_context import MultiComponentUpdateContext
from modules.common.fault_state import FaultState
from modules.sma_shm import counter
from modules.sma_shm import inverter
from modules.sma_shm.speedwire_listener import SpeedwireListener
from modules.sma_shm.utils import SpeedwireComponent


def get_default_config() -> dict:
    return {
        "name": "SMA Smarthome Manager",
        "type": "sma_shm",
        "id": 0,
        "configuration": {}
    }


log = logging.getLogger("SMA Speedwire")
timeout_seconds = 5


class Device(AbstractDevice):
    COMPONENT_FACTORIES = {
        "counter": counter.create_component,
        "inverter": inverter.create_component
    }

    def __init__(self, device_config: dict) -> None:
        self._components = []  # type: List[SpeedwireComponent]
        self.device_config = device_config

    def add_component(self, component_config: dict) -> None:
        try:
            factory = self.COMPONENT_FACTORIES[component_config["type"]]
        except KeyError as e:
            raise Exception(
                "Unknown component type <%s>, known types are: <%s>", e, ','.join(self.COMPONENT_FACTORIES.keys())
            )
        self._components.append(factory(component_config))

    def update(self) -> None:
        log.debug("Beginning update")
        with MultiComponentUpdateContext(self._components):
            if not self._components:
                raise FaultState.warning("Keine Komponenten konfiguriert")

            with SpeedwireListener(timeout_seconds) as speedwire:
                self.__read_speedwire(speedwire)

        log.debug("Update complete")

    def __read_speedwire(self, speedwire: Iterator[dict]):
        stop_time = time.time() + timeout_seconds
        components_todo = self._components
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
        raise FaultState.error("Kein passendes Datagramm innerhalb des %ds timeout empfangen" % timeout_seconds)


def read_legacy(configuration_factory: Callable[[], dict], serial: str, **kwargs):
    device = Device(get_default_config())
    component_config = configuration_factory()
    component_config["configuration"]["serials"] = int(serial) if serial.isnumeric() else None
    component_config.update(kwargs)
    device.add_component(component_config)
    device.update()


def read_legacy_counter(serial: str):
    read_legacy(counter.get_default_config, serial)


def read_legacy_inverter(serial: str, num: int):
    read_legacy(inverter.get_default_config, serial, id=num)


def main(argv: List[str]):
    run_using_positional_cli_args({"counter": read_legacy_counter, "inverter": read_legacy_inverter}, argv)
