#!/usr/bin/env python3
import jq
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.json.config import JsonCounterSetup


class JsonCounter:
    def __init__(self, device_id: int, component_config: Union[Dict, JsonCounterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(JsonCounterSetup, component_config)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response):
        config = self.component_config.configuration

        power = jq.compile(config.jq_power).input(response).first()
        # ToDo: add current or power per phase
        if config.jq_imported == "" or config.jq_exported == "":
            topic_str = "openWB/set/system/device/{}/component/{}/".format(
                self.__device_id, self.component_config.id
            )
            imported, exported = self.__sim_count.sim_count(
                power,
                topic=topic_str,
                data=self.simulation,
                prefix="bezug"
            )
        else:
            imported = jq.compile(config.jq_imported).input(response).first()
            exported = jq.compile(config.jq_exported).input(response).first()

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=JsonCounterSetup)
