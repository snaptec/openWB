#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import req
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.devices.sma_webbox.config import SmaWebboxInverterSetup


class SmaWebboxInverter:
    def __init__(self, device_address: str, component_config: Union[Dict, SmaWebboxInverterSetup]) -> None:
        self.__device_address = device_address
        self.component_config = dataclass_from_dict(SmaWebboxInverterSetup, component_config)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        self.store.set(self.read())

    def read(self) -> InverterState:
        data = {'RPC': '{"version": "1.0","proc": "GetPlantOverview","id": "1","format": "JSON"}'}
        response = req.get_http_session().post(
            'http://' + self.__device_address + '/rpc', data=data, timeout=3).json()

        return InverterState(
            exported=float(response["result"]["overview"][2]["value"]) * 1000,
            power=-int(response["result"]["overview"][0]["value"])
        )


component_descriptor = ComponentDescriptor(configuration_factory=SmaWebboxInverterSetup)
