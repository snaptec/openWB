#!/usr/bin/env python3
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.tesla.http_client import PowerwallHttpClient


def get_default_config() -> dict:
    return {
        "name": "Tesla Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class TeslaInverter:
    def __init__(self, component_config: dict) -> None:
        self.component_config = component_config
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, client: PowerwallHttpClient, aggregate) -> None:
        pv_watt = aggregate["solar"]["instant_power"]
        if pv_watt > 5:
            pv_watt = pv_watt*-1
        self.__store.set(InverterState(
            exported=aggregate["solar"]["energy_exported"],
            power=pv_watt
        ))
