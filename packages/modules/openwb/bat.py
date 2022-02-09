#!/usr/bin/env python3

from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.openwb_flex.bat import BatKitFlex


def get_default_config() -> dict:
    return {
        "name": "Speicher-Kit",
        "type": "bat",
        "id": 0,
        "configuration": {
            "version": 2
        }
    }


class BatKit(BatKitFlex):
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.data = {"config": component_config}
        version = self.data["config"]["configuration"]["version"]
        if version == 0:
            id = 1
            ip_address = '192.168.193.19'
        elif version == 1:
            id = 9
            ip_address = '192.168.193.19'
        elif version == 2:
            id = 117
            ip_address = '192.168.193.15'
        else:
            raise FaultState.error("Version " + str(version) + " unbekannt.")
        self.data["config"]["configuration"]["id"] = id

        super().__init__(device_id, self.data["config"], modbus.ModbusClient(ip_address, 8899))
