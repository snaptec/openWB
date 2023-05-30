#!/usr/bin/env python3
import logging
from typing import Dict, Union


from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.solar_log.config import SolarLogCounterSetup

log = logging.getLogger(__name__)


class SolarLogCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolarLogCounterSetup]) -> None:
        self.component_config = dataclass_from_dict(SolarLogCounterSetup, component_config)
        self.sim_counter = SimCounter(device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response: Dict) -> None:
        self.store_values(self.get_power(response))

    def store_values(self, power) -> None:
        imported, exported = self.sim_counter.sim_count(power)

        self.store.set(CounterState(
            imported=imported,
            exported=exported,
            power=power
        ))

    def get_power(self, response: Dict) -> CounterState:
        return int(float(response["801"]["170"]["110"]))


component_descriptor = ComponentDescriptor(configuration_factory=SolarLogCounterSetup)
