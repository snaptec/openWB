#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.lg.config import LgCounterSetup


class LgCounter:
    def __init__(self, device_id: int, component_config:  Union[Dict, LgCounterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(LgCounterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        power = float(response["statistics"]["grid_power"])
        if response["direction"]["is_grid_selling_"] == "1":
            power = power*-1

        imported, exported = self.sim_counter.sim_count(power)
        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=LgCounterSetup)
