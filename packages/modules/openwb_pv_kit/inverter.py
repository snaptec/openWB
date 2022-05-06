#!/usr/bin/env python3

from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.openwb_flex.inverter import PvKitFlex


def get_default_config() -> dict:
    return {
        "name": "PV-Kit",
        "type": "inverter",
        "id": 0,
        "configuration": {
            "version": 2
        }
    }


class PvKit(PvKitFlex):
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.data = {"config": component_config}
        version = self.data["config"]["configuration"]["version"]
        if version == 0 or version == 1:
            id = 0x08
        elif version == 2:
            id = 116
        else:
            raise FaultState.error("Version "+str(version) + " unbekannt.")
        self.data["config"]["configuration"]["id"] = id

        super().__init__(device_id, self.data["config"], tcp_client)
