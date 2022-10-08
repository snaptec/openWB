#!/usr/bin/env python3
from typing import Any, Callable
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.kostal_plenticore.config import KostalPlenticoreInverterSetup


class KostalPlenticoreInverter:
    def __init__(self, component_config: KostalPlenticoreInverterSetup) -> None:
        self.component_config = component_config
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, reader: Callable[[int, ModbusDataType], Any]) -> InverterState:
        power = min(0, reader(575, ModbusDataType.INT_16))
        exported = reader(320, ModbusDataType.FLOAT_32)

        return InverterState(
            power=power,
            exported=exported
        )

    def dc_in_string_1_2(self, reader):
        return reader(260, ModbusDataType.FLOAT_32) + reader(270, ModbusDataType.FLOAT_32)

    def home_consumption(self, reader):
        return reader(106, ModbusDataType.FLOAT_32)

    def set(self, state):
        self.__store.set(state)


def create_component(component_config: KostalPlenticoreInverterSetup):
    return KostalPlenticoreInverter(component_config)


component_descriptor = ComponentDescriptor(configuration_factory=KostalPlenticoreInverterSetup)
