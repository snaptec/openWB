#!/usr/bin/env python3
from typing import Dict, Union

import jq

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.json.config import JsonBatSetup


class JsonBat:
    def __init__(self, device_id: int, component_config: Union[Dict, JsonBatSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(JsonBatSetup, component_config)
        self.__sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        config = self.component_config.configuration

        power = jq.compile(config.jq_power).input(response).first()
        if config.jq_soc != "":
            soc = jq.compile(config.jq_soc).input(response).first()
        else:
            soc = 0

        if config.jq_imported != "" and config.jq_exported != "":
            imported = jq.compile(config.jq_imported).input(response).first()
            exported = jq.compile(config.jq_exported).input(response).first()
        else:
            imported, exported = self.__sim_counter.sim_count(power)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=JsonBatSetup)
