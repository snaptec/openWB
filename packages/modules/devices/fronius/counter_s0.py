#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.fronius.config import FroniusConfiguration, FroniusS0CounterSetup


class FroniusS0Counter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, FroniusS0CounterSetup],
                 device_config: FroniusConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(FroniusS0CounterSetup, component_config)
        self.device_config = device_config
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        session = req.get_http_session()
        response = session.get(
            'http://'+self.device_config.ip_address+'/solar_api/v1/GetPowerFlowRealtimeData.fcgi',
            timeout=5)
        # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
        power = float(response.json()["Body"]["Data"]["Site"]["P_Grid"]) or 0

        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=FroniusS0CounterSetup)
