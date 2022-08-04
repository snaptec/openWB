#!/usr/bin/env python3
from typing import Dict, Union

import jq

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount._simcounter import SimCounter
from modules.common.store import get_counter_value_store
from modules.json.config import JsonCounterSetup


class JsonCounter:
    def __init__(self, device_id: int, component_config: Union[Dict, JsonCounterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(JsonCounterSetup, component_config)
        self.__sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response):
        config = self.component_config.configuration

        power = jq.compile(config.jq_power).input(response).first()
        # ToDo: add current or power per phase
        if config.jq_imported == "" or config.jq_exported == "":
            imported, exported = self.__sim_counter.sim_count(power)
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
