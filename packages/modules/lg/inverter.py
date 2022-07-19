#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.lg.config import LgInverterSetup


class LgInverter:
    def __init__(self, device_id: int, component_config:  Union[Dict, LgInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(LgInverterSetup, component_config)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, response: Dict) -> None:
        power = float(response["statistics"]["pcs_pv_total_power"]) * -1
        topic_str = "openWB/set/system/device/" + \
            str(self.__device_id)+"/component/" + \
            str(self.component_config.id)+"/"
        _, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.__simulation, prefix="pv")
        inverter_state = InverterState(
            exported=exported,
            power=power
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=LgInverterSetup)
