#!/usr/bin/env python3
from typing import Dict, Union
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store

from modules.batterx.config import BatterXBatSetup
from dataclass_utils import dataclass_from_dict


class BatterXBat:
    def __init__(self, device_id: int, component_config: Union[Dict, BatterXBatSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(BatterXBatSetup, component_config)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.__simulation = {}
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, resp: Dict) -> None:
        power = resp["1121"]["1"]
        soc = resp["1074"]["1"]
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config.id)+"/"
        imported, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.__simulation, prefix="speicher"
        )
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=BatterXBatSetup)
