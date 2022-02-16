#!/usr/bin/env python3
import logging

from modules.common import req
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Wechselrichter Webbox",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


log = logging.getLogger("SMA Webbox")


class SmaWebboxInverter:
    def __init__(self, device_address: str, component_config: dict) -> None:
        self.__device_address = device_address
        self.component_config = component_config
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        self.__store.set(self.read_inverter_state())

    def read_inverter_state(self) -> InverterState:
        log.debug("Komponente "+self.component_config["name"]+" auslesen.")
        data = {'RPC': '{"version": "1.0","proc": "GetPlantOverview","id": "1","format": "JSON"}'}
        response = req.get_http_session().post(
            'http://' + self.__device_address + '/rpc', data=data, timeout=3).json()

        return InverterState(
            counter=float(response["result"]["overview"][2]["value"]) * 1000,
            power=-int(response["result"]["overview"][0]["value"])
        )
