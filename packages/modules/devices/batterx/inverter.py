#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.devices.batterx.config import BatterXInverterSetup
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store


class BatterXInverter:
    def __init__(self, device_id: int, component_config: Union[Dict, BatterXInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(BatterXInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def get_power(self, resp: Dict) -> float:
        return resp["1634"]["0"] * -1

    def get_inverter_state(self, power: float) -> InverterState:
        _, exported = self.sim_counter.sim_count(power)

        return InverterState(
            power=power,
            exported=exported
        )

    def update(self, resp: Dict) -> None:
        self.store.set(self.get_inverter_state(self.get_power(resp)))


component_descriptor = ComponentDescriptor(configuration_factory=BatterXInverterSetup)
