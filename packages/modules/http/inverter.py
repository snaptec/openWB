#!/usr/bin/env python3

from helpermodules import compatibility
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.http.api import create_request_function


def get_default_config() -> dict:
    return {
        "name": "HTTP Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {
            "power_path": None,
            "counter_path": None
        }
    }


class HttpInverter:
    def __init__(self, device_id: int, component_config: dict, url: str) -> None:
        self.__get_power = create_request_function(url, component_config["configuration"]["power_path"])
        self.__get_counter = create_request_function(url, component_config["configuration"]["counter_path"])

        self.__device_id = device_id
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        power = (-self.__get_power() if compatibility.is_ramdisk_in_use() else self.__get_power())
        counter = self.__get_counter()
        if counter is None:
            topic_str = "openWB/set/system/device/" + \
                str(self.__device_id)+"/component/" + \
                str(self.component_config["id"])+"/"
            _, counter = self.__sim_count.sim_count(
                power, topic=topic_str, data=self.simulation, prefix="pv")

        inverter_state = InverterState(
            # for compatibility: in 1.x power URL values are positive!
            power=power,
            counter=counter
        )
        self.__store.set(inverter_state)
