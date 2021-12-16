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
            "power_path": "/power.txt",
            "imported_path": "/imported.txt",
            "exported_path": "/exported.txt",
            "soc_path": "/soc.txt"
        }
    }


class HttpBat:
    def __init__(self, component_config: dict, domain: str) -> None:
        self.component_config = component_config
        self.domain = domain
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        config = self.component_config["configuration"]

        power = request_value(self.domain + config["power_path"])
        imported = request_value(self.domain + config["imported_path"])
        exported = request_value(self.domain + config["exported_path"])
        soc = request_value(self.domain + config["soc_path"])

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
