#!/usr/bin/env python3
from math import copysign

from modules.common.component_state import CounterState
from modules.common.store import get_counter_value_store
from modules.common.component_type import ComponentDescriptor
from modules.devices.sma_shm.config import SmaHomeManagerCounterSetup
from modules.devices.sma_shm.utils import SpeedwireComponent


def parse_datagram(sma_data: dict):
    def get_power(phase_str: str = ""):
        # "consume" and "supply" are always >= 0. Thus we need to check both "supply" and "consume":
        power_import = sma_data["p" + phase_str + "consume"]
        return -sma_data["p" + phase_str + "supply"] if power_import == 0 else power_import

    powers = [get_power(str(phase)) for phase in range(1, 4)]

    counter_state = CounterState(
        imported=sma_data['pconsumecounter'] * 1000,
        exported=sma_data['psupplycounter'] * 1000,
        power=get_power(),
        voltages=[sma_data["u" + str(phase)] for phase in range(1, 4)],
        # currents reported are always absolute values. We get the sign from power:
        currents=[copysign(sma_data["i" + str(phase)], powers[phase - 1]) for phase in range(1, 4)],
        powers=powers,
        power_factors=[sma_data["cosphi" + str(phase)] for phase in range(1, 4)]
    )
    frequency = sma_data.get("frequency")
    if frequency:
        counter_state.frequency = frequency

    return counter_state


def create_component(component_config: SmaHomeManagerCounterSetup):
    return SpeedwireComponent(get_counter_value_store, parse_datagram, component_config)


component_descriptor = ComponentDescriptor(configuration_factory=SmaHomeManagerCounterSetup)
