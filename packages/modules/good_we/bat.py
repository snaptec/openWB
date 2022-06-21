#!/usr/bin/env python3
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "GoodWe Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {}
    }


class GoodWeBat:
    def __init__(self, modbus_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__modbus_id = modbus_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        with self.__tcp_client:
            power = self.__tcp_client.read_holding_registers(35183, ModbusDataType.INT_16, unit=self.__modbus_id)*-1
            soc = self.__tcp_client.read_holding_registers(37007, ModbusDataType.UINT_16, unit=self.__modbus_id)
            imported = self.__tcp_client.read_holding_registers(
                35206, ModbusDataType.UINT_32, unit=self.__modbus_id) * 100
            exported = self.__tcp_client.read_holding_registers(
                35209, ModbusDataType.UINT_32, unit=self.__modbus_id) * 100

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
