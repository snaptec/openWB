#!/usr/bin/env python3
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.http.api import create_request_function


def get_default_config() -> dict:
    return {
        "name": "HTTP Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {
            "power_path": None,
            "imported_path": None,
            "exported_path": None,
            "soc_path": None
        }
    }


class HttpBat:
    def __init__(self, device_id: int, component_config: dict, url: str) -> None:
        self.__get_power = create_request_function(url, component_config["configuration"]["power_path"])
        self.__get_imported = create_request_function(url, component_config["configuration"]["imported_path"])
        self.__get_exported = create_request_function(url, component_config["configuration"]["exported_path"])
        self.__get_soc = create_request_function(url, component_config["configuration"]["soc_path"])

        self.__device_id = device_id
        self.component_config = component_config
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        imported = self.__get_imported()
        exported = self.__get_exported()
        power = self.__get_power()
        if imported is None or exported is None:
            topic_str = "openWB/set/system/device/" + str(
                self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
            imported, exported = self.__sim_count.sim_count(
                power, topic=topic_str, data=self.simulation, prefix="speicher"
            )

        bat_state = BatState(
            power=power,
            soc=self.__get_soc(),
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
