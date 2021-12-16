#!/usr/bin/env python3
from helpermodules import log
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_counter_value_store
from modules.http.api import request_value


def get_default_config() -> dict:
    return {
        "name": "HTTP Zähler",
        "id": 0,
        "type": "counter",
        "configuration":
        {
            "power_all_path": "/power_all.txt",
            "imported_path": "/imported.txt",
            "exported_path": "/exported.txt",
            "power_l1_path": "/power_l1.txt",
            "power_l2_path": "/power_l2.txt",
            "power_l3_path": "/power_l3.txt",
        }
    }


class HttpCounter:
    def __init__(self, component_config: dict, domain: str) -> None:
        self.component_config = component_config
        self.domain = domain
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        config = self.component_config["configuration"]

        power_all = request_value(self.domain + config["power_all_path"])
        imported = request_value(self.domain + config["imported_path"])
        exported = request_value(self.domain + config["exported_path"])
        powers = [request_value(self.domain + config["power_l"+str(i)+"_path"]) for i in range(1, 4)]

        counter_state = CounterState(
            powers=powers,
            imported=imported,
            exported=exported,
            power_all=power_all
        )
        self.__store.set(counter_state)
