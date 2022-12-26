#!/usr/bin/env python3
from typing import Dict, Union

import jq

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.json.config import JsonInverterSetup


class JsonInverter:
    def __init__(self, device_id: int, component_config: Union[Dict, JsonInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(JsonInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        config = self.component_config.configuration

        power = float(jq.compile(config.jq_power).input(response).first())
        if power >= 0:
            power = power * -1
        if config.jq_exported is None:
            _, exported = self.sim_counter.sim_count(power)
        else:
            exported = float(jq.compile(config.jq_exported).input(response).first())

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=JsonInverterSetup)
