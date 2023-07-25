#!/usr/bin/env python3
import logging
from typing import Dict, Union
from requests import Session


from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.smart_me.config import SmartMeInverterSetup

log = logging.getLogger(__name__)


class SmartMeInverter:
    def __init__(self,
                 component_config: Union[Dict, SmartMeInverterSetup]) -> None:
        self.component_config = dataclass_from_dict(SmartMeInverterSetup, component_config)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, session: Session) -> None:
        response = session.get('https://smart-me.com:443/api/Devices/' +
                               self.component_config.configuration.id, timeout=3).json()

        self.store.set(InverterState(
            exported=response["CounterReadingExport"] * 1000,
            power=response["ActivePower"] * 1000,
        ))


component_descriptor = ComponentDescriptor(configuration_factory=SmartMeInverterSetup)
