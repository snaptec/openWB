#!/usr/bin/env python3

from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store
from modules.common.component_type import ComponentDescriptor
from modules.devices.sma_shm.config import SmaHomeManagerInverterSetup
from modules.devices.sma_shm.utils import SpeedwireComponent


def parse_datagram(sma_data: dict):
    return InverterState(
        power=-int(sma_data['psupply']),
        exported=sma_data['psupplycounter'] * 1000
    )


def create_component(component_config: SmaHomeManagerInverterSetup):
    return SpeedwireComponent(get_inverter_value_store, parse_datagram, component_config)


component_descriptor = ComponentDescriptor(configuration_factory=SmaHomeManagerInverterSetup)
