#!/usr/bin/env python3

import requests
from requests.auth import HTTPDigestAuth

from helpermodules import log
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store

"""Example Output for ajax.txt
109 W;103 W;111 VA;41 var;333.8;223.2;0.3;0.5;109.0;103.0;---;---;0.93 c;1.60;105.2;190.2;55342.2;132;0;0;NT 5000;1;
x
00200403;01;00000001
"""


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
        params = (
            ('CAN', '1'),
            ('HASH', '00200403'),
            ('TYPE', '1'),
        )
        response = requests.get("http://" + self.ip_address + "/data/ajax.txt", params=params,
                                auth=HTTPDigestAuth("customer", self.password))
        log.MainLogger().debug("API Response: %s" % (str(response.text)))
        response.raise_for_status()
        values = response.text.split(';')

        inverter_state = InverterState(
            power=float(values[1].split(' ')[0]),
            counter=float(values[16])*1000
        )
        self.__store.set(inverter_state)
