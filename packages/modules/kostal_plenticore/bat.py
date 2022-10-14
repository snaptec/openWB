#!/usr/bin/env python3
from typing import Any, Callable
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.kostal_plenticore.config import KostalPlenticoreBatSetup


class KostalPlenticoreBat:
    def __init__(self,
                 device_id: int,
                 component_config: KostalPlenticoreBatSetup) -> None:
        self.component_config = component_config
        self.store = get_bat_value_store(self.component_config.id)
        self.sim_counter = SimCounter(device_id, self.component_config.id, prefix="speicher")
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, reader: Callable[[int, ModbusDataType], Any]) -> BatState:
        power = reader(582, ModbusDataType.INT_16)
        soc = reader(514, ModbusDataType.INT_16)
        imported, exported = self.sim_counter.sim_count(power)

        return BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported,
        )

    def set(self, state):
        self.store.set(state)


component_descriptor = ComponentDescriptor(configuration_factory=KostalPlenticoreBatSetup)
