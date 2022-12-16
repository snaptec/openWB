#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.solar_watt.api import parse_value
from modules.devices.solar_watt.config import SolarWattInverterSetup

log = logging.getLogger(__name__)


class SolarWattInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolarWattInverterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SolarWattInverterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response: Dict) -> None:
        power = parse_value(response, "PowerProduced") * -1
        _, exported = self.sim_counter.sim_count(power)
        self.store.set(InverterState(
            exported=exported,
            power=power
        ))


component_descriptor = ComponentDescriptor(configuration_factory=SolarWattInverterSetup)
