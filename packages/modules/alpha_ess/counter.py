#!/usr/bin/env python3
import time
from typing import Callable

from helpermodules import log
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS Zähler",
        "id": 0,
        "type": "counter",
        "configuration": {
            "version": 1
        }
    }


class AlphaEssCounter:
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__store = get_counter_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self, unit_id: int):
        log.MainLogger().debug(
            "Komponente "+self.component_config["name"]+" auslesen.")
        time.sleep(0.1)
        factory_method = self.__get_values_factory(
            self.component_config["configuration"]["version"])
        counter_state = factory_method(unit=unit_id)
        self.__store.set(counter_state)

    def __get_values_factory(self, version: int) -> Callable[[int], CounterState]:
        return self.__get_values_before_v123 if version == 0 else self.__get_values_since_v123

    def __get_values_before_v123(self, unit: int) -> CounterState:
        with self.__tcp_client:
            power, exported, imported = self.__tcp_client.read_holding_registers(
                0x6, [modbus.ModbusDataType.INT_32] * 3, unit=unit)
            exported *= 10
            imported *= 10
            currents = [val / 230 for val in self.__tcp_client.read_holding_registers(
                0x0000, [ModbusDataType.INT_32]*3, unit=unit)]

        counter_state = CounterState(
            currents=currents,
            imported=imported,
            exported=exported,
            power=power
        )
        return counter_state

    def __get_values_since_v123(self, unit: int) -> CounterState:
        with self.__tcp_client:
            power = self.__tcp_client.read_holding_registers(
                0x0021, ModbusDataType.INT_32, unit=unit)
            exported = self.__tcp_client.read_holding_registers(
                0x0010, ModbusDataType.INT_32, unit=unit) * 10
            imported = self.__tcp_client.read_holding_registers(
                0x0012, ModbusDataType.INT_32, unit=unit) * 10
            currents = [val / 1000 for val in self.__tcp_client.read_holding_registers(
                0x0017, [ModbusDataType.INT_16]*3, unit=unit)]

        counter_state = CounterState(
            currents=currents,
            imported=imported,
            exported=exported,
            power=power
        )
        return counter_state
