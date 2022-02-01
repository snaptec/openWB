#!/usr/bin/env python3
from helpermodules import log
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "Sunny Island Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {}
    }


class SunnyIslandBat:
    def __init__(self, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        log.MainLogger().debug("Komponente "+self.component_config["name"]+" auslesen.")
        unit = 3
        with self.__tcp_client:
            soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.INT_32, unit=unit)
            power = self.__tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=unit) * -1
            [imported, exported] = self.__tcp_client.read_holding_registers(30595, [ModbusDataType.INT_32]*2, unit=unit)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
