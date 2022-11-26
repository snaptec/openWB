#!/usr/bin/env python3
from typing import Dict, Union

import jq

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.json.config import JsonBatSetup


class JsonBat:
    def __init__(self, device_id: int, component_config: Union[Dict, JsonBatSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(JsonBatSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        config = self.component_config.configuration

        power = float(jq.compile(config.jq_power).input(response).first())
        if config.jq_soc != "":
            soc = float(jq.compile(config.jq_soc).input(response).first())
        else:
            soc = 0

        if config.jq_imported is not None and config.jq_exported is not None:
            imported = float(jq.compile(config.jq_imported).input(response).first())
            exported = float(jq.compile(config.jq_exported).input(response).first())
        else:
            imported, exported = self.sim_counter.sim_count(power)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=JsonBatSetup)
