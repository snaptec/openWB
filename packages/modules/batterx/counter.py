#!/usr/bin/env python3
import logging
from typing import Dict, List, Union

from dataclass_utils import dataclass_from_dict
from modules.common.store import get_counter_value_store
from modules.common.fault_state import ComponentInfo
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common import simcount
from modules.batterx.config import BatterXCounterSetup

log = logging.getLogger(__name__)


class BatterXCounter:
    def __init__(self, device_id: int, component_config: Union[Dict, BatterXCounterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(BatterXCounterSetup, component_config)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

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
        topic_str = "openWB/set/system/device/{}/component/{}/".format(
            self.__device_id, self.component_config.id
        )
        imported, exported = self.__sim_count.sim_count(
            power,
            topic=topic_str,
            data=self.simulation,
            prefix="bezug"
        )

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
        self.__store.set(counter_state)

    def __parse_list_values(self, resp_json: Dict,
                            id: int, factor: int = 1) -> List[float]:
        return [resp_json[str(id+i)]["0"] / factor for i in range(0, 3)]


component_descriptor = ComponentDescriptor(configuration_factory=BatterXCounterSetup)
