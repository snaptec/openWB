#!/usr/bin/env python3
from typing import Dict, List, Tuple, Union
import logging

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.common import req
from modules.common import simcount
from modules.kostal_piko.config import KostalPikoCounterSetup

log = logging.getLogger(__name__)


class KostalPikoCounter:
    def __init__(self, device_id: int, component_config: Union[Dict, KostalPikoCounterSetup], ip_address: str) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(KostalPikoCounterSetup, component_config)
        self.ip_address = ip_address
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def get_values(self) -> Tuple[float, List[float]]:
        params = (('dxsEntries', ['83887106', '83887362', '83887618']),)
        resp = req.get_http_session().get('http://'+self.ip_address+'/api/dxs.json',
                                          params=params,
                                          timeout=3).json()["dxsEntries"]
        powers = [float(resp[0]["value"]), float(resp[1]["value"]), float(resp[2]["value"])]
        home_consumption = sum(powers)
        return home_consumption, powers

    def update(self):
        power, powers = self.get_values()
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
            powers=powers
        )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=KostalPikoCounterSetup)
