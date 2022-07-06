#!/usr/bin/env python3
import logging
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Sunny Island Speicher",
        "id": 0,
        "type": "bat",
        "configuration": {}
    }


log = logging.getLogger(__name__)


class SunnyIslandBat:
    def __init__(self, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def read(self) -> BatState:
        unit = 3
        with self.__tcp_client:
            soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.INT_32, unit=unit)

            power = self.__tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=unit) * -1
            imported, exported = self.__tcp_client.read_holding_registers(30595, [ModbusDataType.INT_32]*2, unit=unit)

        return BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )

    def update(self) -> None:
        self.__store.set(self.read())
