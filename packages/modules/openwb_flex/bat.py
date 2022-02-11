#!/usr/bin/env python3

from helpermodules import log
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.openwb_flex.versions import kit_bat_version_factory


def get_default_config() -> dict:
    return {
        "name": "Speicher-Kit flex",
        "type": "bat",
        "id": None,
        "configuration": {
            "version": 2,
            "id": 117
        }
    }


class BatKitFlex:
    def __init__(self, device_id: int, component_config: dict,
                 tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        factory = kit_bat_version_factory(
            component_config["configuration"]["version"])
        self.__client = factory(component_config["configuration"]["id"],
                                tcp_client)
        self.__tcp_client = tcp_client
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        log.MainLogger().debug("Start kit reading")
        # TCP-Verbindung schließen möglichst bevor etwas anderes gemacht wird, um im Fehlerfall zu verhindern,
        # dass offene Verbindungen den Modbus-Adapter blockieren.
        with self.__tcp_client:
            imported = self.__client.get_imported()
            exported = self.__client.get_exported()
            if self.component_config["configuration"]["version"] == 2:
                _, power = self.__client.get_power()
                power = power * -1
            else:
                _, power = self.__client.get_power()

        bat_state = BatState(
            imported=imported,
            exported=exported,
            power=power
        )
        log.MainLogger().debug("Speicher-Kit Leistung[W]: " + str(bat_state.power))
        self.__store.set(bat_state)
