#!/usr/bin/env python3
from typing import Dict, Union

from requests import Session

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.http.api import create_request_function, create_request_function_array
from modules.devices.http.config import HttpCounterSetup


class HttpCounter:
    def __init__(self, device_id: int, component_config: Union[Dict, HttpCounterSetup], url: str) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(HttpCounterSetup, component_config)
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

        self.__get_power = create_request_function(url, self.component_config.configuration.power_path)
        self.__get_imported = create_request_function(url, self.component_config.configuration.imported_path)
        self.__get_exported = create_request_function(url, self.component_config.configuration.exported_path)
        self.__get_currents = create_request_function_array(url, [
            component_config.configuration.current_l1_path,
            component_config.configuration.current_l2_path,
            component_config.configuration.current_l3_path,
        ])

    def update(self, session: Session) -> None:
        power = self.__get_power(session)
        exported = self.__get_exported(session)
        imported = self.__get_imported(session)
        if imported is None or exported is None:
            imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            power=power,
            exported=exported,
            imported=imported,
            currents=self.__get_currents(session)
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=HttpCounterSetup)
