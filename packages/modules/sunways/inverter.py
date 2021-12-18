#!/usr/bin/env python3

import requests
from requests.auth import HTTPDigestAuth

from helpermodules import log
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "Sunways Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class SunwaysInverter:
    def __init__(self, component_config: dict, ip_address: str, password: str) -> None:
        self.component_config = component_config
        self.ip_address = ip_address
        self.password = password
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")

        response = requests.get(
            "http://" + self.ip_address + "/data/ajax.txt?CAN=1", auth=HTTPDigestAuth("customer", self.password)
        )
        response.raise_for_status()
        log.MainLogger().debug("API Response: %s", response.text)
        values = response.text.split(';')

        inverter_state = InverterState(
            power=float(values[1]),
            counter=float(values[16])*1000
        )
        self.__store.set(inverter_state)
