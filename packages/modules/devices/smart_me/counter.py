#!/usr/bin/env python3
import logging
from typing import Dict, List, Union
from requests import Session


from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.devices.smart_me.config import SmartMeCounterSetup

log = logging.getLogger(__name__)


class SmartMeCounter:
    def __init__(self,
                 component_config: Union[Dict, SmartMeCounterSetup]) -> None:
        self.component_config = dataclass_from_dict(SmartMeCounterSetup, component_config)
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, session: Session) -> None:
        def parse_phase_values(key: str) -> List[float]:
            return [response[key+str(i)] for i in range(1, 4)]

        response = session.get('https://smart-me.com:443/api/Devices/' +
                               self.component_config.configuration.id, timeout=3).json()

        currents = parse_phase_values("CurrentL")
        if currents[0] is None:
            currents[0] = response["Current"]

        powers = parse_phase_values("ActivePowerL")
        powers = [powers[i] * 1000 for i in range(0, 3)]
        if powers[0] == 0:
            powers[0] = response["ActivePower"]

        self.store.set(CounterState(
            imported=response["CounterReadingImport"] * 1000,
            exported=response["CounterReadingExport"] * 1000,
            power=response["ActivePower"] * 1000,
            powers=powers,
            currents=currents,
            power_factors=parse_phase_values("PowerFactorL"),
            voltages=parse_phase_values("VoltageL")
        ))


component_descriptor = ComponentDescriptor(configuration_factory=SmartMeCounterSetup)
