#!/usr/bin/env python3
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "GoodWe Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {}
    }


class GoodWeCounter:
    def __init__(self, modbus_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__modbus_id = modbus_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        with self.__tcp_client:
            power_factors = [
                val / 1000 for val in self.__tcp_client.read_holding_registers(36010,
                                                                               [ModbusDataType.UINT_16]*3,
                                                                               unit=self.__modbus_id)]
            exported = self.__tcp_client.read_holding_registers(
                36015, ModbusDataType.FLOAT_32, unit=self.__modbus_id)
            imported = self.__tcp_client.read_holding_registers(
                36017, ModbusDataType.FLOAT_32, unit=self.__modbus_id)
            powers = [
                val * -1 for val in self.__tcp_client.read_holding_registers(36005,
                                                                             [ModbusDataType.INT_16]*3,
                                                                             unit=self.__modbus_id)]
            power = self.__tcp_client.read_holding_registers(36008, ModbusDataType.INT_16, unit=self.__modbus_id) * -1

            frequency = self.__tcp_client.read_holding_registers(
                36014, ModbusDataType.UINT_16, unit=self.__modbus_id) / 100

        counter_state = CounterState(
            powers=powers,
            imported=imported,
            exported=exported,
            power=power,
            power_factors=power_factors,
            frequency=frequency
        )
        self.__store.set(counter_state)
