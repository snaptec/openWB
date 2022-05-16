#!/usr/bin/env python3
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.tesla.http_client import PowerwallHttpClient


def get_default_config() -> dict:
    return {
        "name": "Tesla Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {}
    }


class TeslaBat:
    def __init__(self, component_config: dict) -> None:
        self.component_config = component_config
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, client: PowerwallHttpClient, aggregate) -> None:
        self.__store.set(BatState(
            imported=aggregate["battery"]["energy_imported"],
            exported=aggregate["battery"]["energy_exported"],
            power=-aggregate["battery"]["instant_power"],
            soc=client.get_json("/api/system_status/soe")["percentage"]
        ))
