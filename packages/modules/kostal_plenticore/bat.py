#!/usr/bin/env python3
from typing import Any, Callable
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.kostal_plenticore.config import KostalPlenticoreBatSetup


class KostalPlenticoreBat:
    def __init__(self, component_config: KostalPlenticoreBatSetup) -> None:
        self.component_config = component_config
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, reader: Callable[[int, ModbusDataType], Any]) -> BatState:
        power = reader(582, ModbusDataType.INT_16)
        soc = reader(514, ModbusDataType.INT_16)

        return BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported,
        )

    def set(self, state):
        self.__store.set(state)


def create_component(component_config: KostalPlenticoreBatSetup):
    return KostalPlenticoreBat(component_config)


component_descriptor = ComponentDescriptor(configuration_factory=KostalPlenticoreBatSetup)
