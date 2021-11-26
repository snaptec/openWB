#!/usr/bin/env python3


try:
    from ..common import modbus
    from ..common.fault_state import FaultState
    from ..openwb_flex.counter import EvuKitFlex
except (ImportError, ValueError, SystemError):
    from modules.common import modbus
    from modules.common.fault_state import FaultState
    from modules.openwb_flex.counter import EvuKitFlex


def get_default_config() -> dict:
    return {
        "name": "EVU-Kit",
        "type": "counter",
        "id": 0,
        "configuration":
            {
                "version": 2
            }
    }


class EvuKit(EvuKitFlex):
    def __init__(self, device_id: int, component_config: dict) -> None:
        self.data = {"config": component_config}
        version = self.data["config"]["configuration"]["version"]
        if version == 0:
            id = 5
        elif version == 1:
            id = 2
        elif version == 2:
            id = 115
        else:
            raise FaultState.error("Version " + str(version) + " unbekannt.")
        self.data["config"]["configuration"]["id"] = id

        super().__init__(device_id, self.data["config"], modbus.ModbusClient("192.168.193.15", 8899))
