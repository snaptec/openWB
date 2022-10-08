#!/usr/bin/env python3
from typing import Any, Callable
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.kostal_plenticore.config import KostalPlenticoreCounterSetup


class KostalPlenticoreCounter:
    def __init__(self, component_config: KostalPlenticoreCounterSetup) -> None:
        self.component_config = component_config
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, reader: Callable[[int, ModbusDataType], Any]) -> None:
        power_factor = reader(150, ModbusDataType.FLOAT_32)
        currents = [reader(register, ModbusDataType.FLOAT_32) for register in [222, 232, 242]]
        voltages = [reader(register, ModbusDataType.FLOAT_32) for register in [230, 240, 250]]
        powers = [reader(register, ModbusDataType.FLOAT_32) for register in [224, 234, 244]]
        power = reader(252, ModbusDataType.FLOAT_32)
        frequency = reader(220, ModbusDataType.FLOAT_32)

        counter_state = CounterState(
            powers=powers,
            currents=currents,
            voltages=voltages,
            imported=imported,
            exported=exported,
            power=power,
            power_factors=[power_factor]*3,
            frequency=frequency
        )
        self.__store.set(counter_state)


def create_component(component_config: KostalPlenticoreCounterSetup):
    return KostalPlenticoreCounter(component_config)


component_descriptor = ComponentDescriptor(configuration_factory=KostalPlenticoreCounterSetup)
