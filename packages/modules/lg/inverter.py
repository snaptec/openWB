#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.lg.config import LgInverterSetup


class LgInverter:
    def __init__(self, device_id: int, component_config:  Union[Dict, LgInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(LgInverterSetup, component_config)
        topic_str = "openWB/set/system/device/" + \
            str(self.__device_id)+"/component/" + \
            str(self.component_config.id)+"/"
        self.__sim_counter = SimCounter(topic=topic_str, prefix="pv")
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response: Dict) -> None:
        power = float(response["statistics"]["pcs_pv_total_power"]) * -1
        _, exported = self.__sim_counter.sim_count(power)
        inverter_state = InverterState(
            exported=exported,
            power=power
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=LgInverterSetup)
