#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.solar_watt.api import parse_value
from modules.devices.solar_watt.config import SolarWattCounterSetup

log = logging.getLogger(__name__)


class SolarWattCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolarWattCounterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SolarWattCounterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response: Dict, energy_manager: bool) -> None:
        if energy_manager:
            power_consumed = parse_value(response, "PowerConsumedFromGrid")
            power_out = parse_value(response, "PowerOut")
            power = power_consumed - power_out
        else:
            power = int(response["FData"]["PGrid"])
        imported, exported = self.sim_counter.sim_count(power)
        self.store.set(CounterState(
            imported=imported,
            exported=exported,
            power=power
        ))


component_descriptor = ComponentDescriptor(configuration_factory=SolarWattCounterSetup)
