#!/usr/bin/env python3

from typing import Dict
from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.openwb_flex.bat import BatKitFlex


def get_default_config() -> dict:
    return {
        "name": "Speicher-Kit",
        "type": "bat",
        "id": 0,
        "configuration": {}
    }


class BatKit(BatKitFlex):
    def __init__(self, device: Dict, component_config: Dict, tcp_client: modbus.ModbusClient) -> None:
        self.data = {"config": component_config}
        version = device["configuration"]["version"]
        if version == 0:
            id = 1
        elif version == 1:
            id = 9
        elif version == 2:
            id = 117
        else:
            raise FaultState.error("Version " + str(version) + " unbekannt.")
        self.data["config"]["configuration"]["id"] = id

        super().__init__(device["id"], self.data["config"], tcp_client)
