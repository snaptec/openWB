#!/usr/bin/env python3
from helpermodules import log
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
            "power_path": "/power.txt",
            "imported_path": "/imported.txt",
            "exported_path": "/exported.txt",
            "soc_path": "/soc.txt"
        }
    }


class HttpBat:
    def __init__(self, component_config: dict, domain: str) -> None:
        self.__get_power = create_request_function(domain, component_config["configuration"]["power_path"])
        self.__get_imported = create_request_function(domain, component_config["configuration"]["imported_path"])
        self.__get_exported = create_request_function(domain, component_config["configuration"]["exported_path"])
        self.__get_soc = create_request_function(domain, component_config["configuration"]["soc_path"])

        self.component_config = component_config
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        bat_state = BatState(
            power=self.__get_power(),
            soc=self.__get_soc(),
            imported=self.__get_imported(),
            exported=self.__get_exported()
        )
        self.__store.set(bat_state)
