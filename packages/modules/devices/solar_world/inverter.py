#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.solar_world.config import SolarWorldInverterSetup


class SolarWorldInverter:
    def __init__(self, device_id: int, component_config: Union[Dict, SolarWorldInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SolarWorldInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response) -> None:
        try:
            power = response["PowerTotalPV"] * -1
        except ValueError:
            # wenn eManager aus bzw. keine Antwort ersetze leeren Wert durch eine 0
            power = 0
        exported = self.sim_counter.sim_count(power)[1]

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SolarWorldInverterSetup)
