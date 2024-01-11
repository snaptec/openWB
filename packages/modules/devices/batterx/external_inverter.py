#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.devices.batterx.config import BatterXExternalInverterSetup
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store


class BatterXExternalInverter:
    def __init__(self, device_id: int, component_config: Union[Dict, BatterXExternalInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(BatterXExternalInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def get_power(self, resp: Dict) -> float:
        return resp["2913"]["3"] * -1

    def update(self, resp: Dict) -> None:
        power = self.get_power(resp)

        _, exported = self.sim_counter.sim_count(power)

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=BatterXExternalInverterSetup)
