#!/usr/bin/env python3
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Sunny Boy Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {}
    }


class SunnyBoyBat:
    def __init__(self, device_id: int, component_config: dict, tcp_client: ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def read(self) -> BatState:
        unit = 3
        with self.__tcp_client:
            soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.UINT_32, unit=unit)
            imp = self.__tcp_client.read_holding_registers(31393, ModbusDataType.INT_32, unit=unit)
            exp = self.__tcp_client.read_holding_registers(31395, ModbusDataType.INT_32, unit=unit)
            if imp > 5:
                power = imp
            else:
                power = exp * -1

        exported = self.__tcp_client.read_holding_registers(31401, ModbusDataType.UINT_64, unit=3)
        imported = self.__tcp_client.read_holding_registers(31397, ModbusDataType.UINT_64, unit=3)

        return BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )

    def update(self) -> None:
        self.__store.set(self.read())
