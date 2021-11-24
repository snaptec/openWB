#!/usr/bin/env python3


try:
    from ..common import modbus
    from ..common.abstract_component import ComponentUpdater
    from ..common.module_error import ModuleError, ModuleErrorLevel
    from ..openwb_flex.counter import EvuKitFlex
    from ..common.store import get_counter_value_store
except (ImportError, ValueError, SystemError):
    from modules.common import modbus
    from modules.common.abstract_component import ComponentUpdater
    from modules.common.module_error import ModuleError, ModuleErrorLevel
    from modules.openwb_flex.counter import EvuKitFlex
    from modules.common.store import get_counter_value_store


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


def create_component(device_config: dict, component_config: dict, modbus_client):
    return ComponentUpdater(
            EvuKit(device_config["id"], component_config,
                   modbus.ModbusClient("192.168.193.15", 8899)),
            get_counter_value_store(component_config["id"]))


class EvuKit(EvuKitFlex):
    def __init__(self, device_id: int, component_config: dict,
                 tcp_client: modbus.ModbusClient) -> None:
        self.data = {"config": component_config}
        version = self.data["config"]["configuration"]["version"]
        if version == 0:
            id = 5
        elif version == 1:
            id = 2
        elif version == 2:
            id = 115
        else:
            raise ModuleError("Version " + str(version) + " unbekannt.", ModuleErrorLevel.ERROR)
        self.data["config"]["configuration"]["id"] = id

        super().__init__(device_id, self.data["config"], tcp_client)
