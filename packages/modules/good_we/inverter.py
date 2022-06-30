#!/usr/bin/env python3
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store


def get_default_config() -> dict:
    return {
        "name": "GoodWe Wechselrichter",
        "id": 0,
        "type": "inverter",
        "configuration": {}
    }


class GoodWeInverter:
    def __init__(self, modbus_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.__modbus_id = modbus_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_inverter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        with self.__tcp_client:
            power = sum([self.__tcp_client.read_holding_registers(reg, ModbusDataType.UINT_32,
                        unit=self.__modbus_id) for reg in [35105, 35109, 35113, 35117]]) * -1
            exported = self.__tcp_client.read_holding_registers(
                35191, ModbusDataType.UINT_32, unit=self.__modbus_id) * 100

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.__store.set(inverter_state)
