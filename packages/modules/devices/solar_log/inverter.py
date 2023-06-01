#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.solar_log.config import SolarLogInverterSetup

log = logging.getLogger(__name__)


class SolarLogInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolarLogInverterSetup]) -> None:
        self.component_config = dataclass_from_dict(SolarLogInverterSetup, component_config)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, response: Dict) -> None:
        self.store.set(self.get_values(response))

    def get_values(self, response: Dict) -> InverterState:
        return InverterState(
            exported=float(response["801"]["170"]["109"]),
            power=-abs(float(response["801"]["170"]["101"]))
        )


component_descriptor = ComponentDescriptor(configuration_factory=SolarLogInverterSetup)
