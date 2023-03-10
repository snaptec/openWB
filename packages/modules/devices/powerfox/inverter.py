#!/usr/bin/env python3
import logging
from typing import Dict, Union
from requests import Session


from dataclass_utils import dataclass_from_dict
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.powerfox.config import PowerfoxInverterSetup

log = logging.getLogger(__name__)


class PowerfoxInverter:
    def __init__(self,
                 component_config: Union[Dict, PowerfoxInverterSetup]) -> None:
        self.component_config = dataclass_from_dict(PowerfoxInverterSetup, component_config)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, session: Session) -> None:
        response = session.get('https://backend.powerfox.energy/api/2.0/my/'+self.component_config.configuration.id +
                               '/current', timeout=3).json()

        self.store.set(InverterState(
            exported=float(response['A_Plus']),
            power=float(response['Watt'])
        ))


component_descriptor = ComponentDescriptor(configuration_factory=PowerfoxInverterSetup)
