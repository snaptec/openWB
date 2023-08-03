#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.solar_watt.api import parse_value
from modules.devices.solar_watt.config import SolarWattBatSetup

log = logging.getLogger(__name__)


class SolarWattBat:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolarWattBatSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SolarWattBatSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response: Dict, energy_manager: bool) -> None:
        if energy_manager:
            exported_temp = parse_value(response, "PowerConsumedFromStorage")
            imported_temp = parse_value(response, "PowerOutFromStorage")
            inside_temp = parse_value(response, "PowerBuffered")
            power = (exported_temp + imported_temp - inside_temp) * -1
            soc = parse_value(response, "StateOfCharge")
        else:
            power = response["FData"]["IBat"] * response["FData"]["VBat"] * -1
            soc = response["SData"]["SoC"]
        imported, exported = self.sim_counter.sim_count(power)
        self.store.set(BatState(
            imported=imported,
            exported=exported,
            power=power,
            soc=soc
        ))


component_descriptor = ComponentDescriptor(configuration_factory=SolarWattBatSetup)
