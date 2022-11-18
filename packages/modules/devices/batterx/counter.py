#!/usr/bin/env python3
import logging
from typing import Dict, List, Union

from dataclass_utils import dataclass_from_dict
from modules.devices.batterx.config import BatterXCounterSetup
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store

log = logging.getLogger(__name__)


class BatterXCounter:
    def __init__(self, device_id: int, component_config: Union[Dict, BatterXCounterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(BatterXCounterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, resp: Dict) -> None:
        power = resp["2913"]["0"]
        frequency = resp["2914"]["0"] / 100
        powers = self.__parse_list_values(resp, 2897)
        voltages = self.__parse_list_values(resp, 2833, 100)
        currents = self.__parse_list_values(resp, 2865, 100)
        try:
            power_factors = self.__parse_list_values(resp, 2881)
        except KeyError:
            log.debug(
                "Powerfaktor sollte laut Doku enthalten sein, ID 2881 kann aber nicht ermittelt werden.")
            power_factors = None
        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power,
            powers=powers,
            currents=currents,
            voltages=voltages,
            frequency=frequency
        )
        if power_factors:
            counter_state.power_factors = power_factors
        self.store.set(counter_state)

    def __parse_list_values(self, resp_json: Dict,
                            id: int, factor: int = 1) -> List[float]:
        return [resp_json[str(id+i)]["0"] / factor for i in range(0, 3)]


component_descriptor = ComponentDescriptor(configuration_factory=BatterXCounterSetup)
