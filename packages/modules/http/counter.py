#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.http.api import create_request_function
from modules.http.config import HttpCounterSetup


class HttpCounter:
    def __init__(self, device_id: int, component_config: Union[Dict, HttpCounterSetup], url: str) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(HttpCounterSetup, component_config)
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

        self.__get_power = create_request_function(url, self.component_config.configuration.power_path)
        self.__get_imported = create_request_function(url, self.component_config.configuration.imported_path)
        self.__get_exported = create_request_function(url, self.component_config.configuration.exported_path)
        self.__get_currents = [
            create_request_function(url,
                                    getattr(self.component_config.configuration, "current_l" + str(i) + "_path"))
            for i in range(1, 4)
        ]

    def update(self):
        imported = self.__get_imported()
        exported = self.__get_exported()
        power = self.__get_power()
        if imported is None or exported is None:
            topic_str = "openWB/set/system/device/{}/component/{}/".format(
                self.__device_id, self.component_config.id
            )
            imported, exported = self.__sim_count.sim_count(
                power,
                topic=topic_str,
                data=self.simulation,
                prefix="bezug"
            )

        counter_state = CounterState(
            currents=[getter() for getter in self.__get_currents],
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=HttpCounterSetup)
