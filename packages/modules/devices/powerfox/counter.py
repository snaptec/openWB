#!/usr/bin/env python3
import logging
from typing import Dict, Union
from requests import Session


from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.devices.powerfox.config import PowerfoxCounterSetup

log = logging.getLogger(__name__)


class PowerfoxCounter:
    def __init__(self,
                 component_config: Union[Dict, PowerfoxCounterSetup]) -> None:
        self.component_config = dataclass_from_dict(PowerfoxCounterSetup, component_config)
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, session: Session) -> None:
        response = session.get('https://backend.powerfox.energy/api/2.0/my/'+self.component_config.configuration.id +
                               '/current', timeout=3).json()

        self.store.set(CounterState(
            imported=float(response['A_Plus']),
            exported=float(response['A_Minus']),
            power=float(response['Watt'])
        ))


component_descriptor = ComponentDescriptor(configuration_factory=PowerfoxCounterSetup)
