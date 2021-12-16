#!/usr/bin/env python3

from helpermodules import log
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.http.api import request_value


def get_default_config() -> dict:
    return {
        "name": "HTTP Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration":
        {
            "power_path": "/power.txt",
            "counter_path": "/counter.txt",
        }
    }


class HttpInverter:
    def __init__(self, component_config: dict, domain: str) -> None:
        self.component_config = component_config
        self.domain = domain
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        config = self.component_config["configuration"]

        power = request_value(self.domain + config["power_path"])
        counter = request_value(self.domain + config["counter_path"])

        inverter_state = InverterState(
            power=power,
            counter=counter
        )
        self.__store.set(inverter_state)
