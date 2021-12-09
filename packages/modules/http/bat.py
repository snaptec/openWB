#!/usr/bin/env python3
from helpermodules import log
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.http.api import request_value


def get_default_config() -> dict:
    return {
        "name": "HTTP Speicher",
        "id": 0,
        "type": "bat",
        "configuration":
        {
            "power_url": "/power.txt",
            "imported_url": "/imported.txt",
            "exported_url": "/exported.txt",
            "soc_url": "/soc.txt"
        }
    }


class HttpBat:
    def __init__(self, component_config: dict, ip_address: str) -> None:
        self.component_config = component_config
        self.ip_address = ip_address
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        config = self.component_config["configuration"]

        power = request_value(self.ip_address + config["power_url"])
        imported = request_value(self.ip_address + config["imported_url"])
        exported = request_value(self.ip_address + config["exported_url"])
        soc = request_value(self.ip_address + config["soc_url"])

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
