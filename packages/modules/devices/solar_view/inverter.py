#!/usr/bin/env python3
import logging
from typing import Dict, Union


from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.solar_view.api import request
from modules.devices.solar_view.config import SolarViewInverterSetup

log = logging.getLogger(__name__)


class SolarViewInverter:
    def __init__(self, component_config: Union[Dict, SolarViewInverterSetup]) -> None:
        self.component_config = dataclass_from_dict(SolarViewInverterSetup, component_config)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, ip_address: str, port: int, timeout: int) -> None:
        values = request(ip_address, port, timeout, self.component_config.configuration.command)
        self.store.set(InverterState(
            exported=1000 * int(values[9]),
            power=-1 * int(values[10])
        ))


component_descriptor = ComponentDescriptor(configuration_factory=SolarViewInverterSetup)
