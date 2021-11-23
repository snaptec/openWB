#!/usr/bin/env python3
import time
from typing import Callable, List, Tuple

try:
    from ...helpermodules import log
    from ..common import modbus
    from ..common.abstract_component import AbstractCounter
    from ..common.component_state import CounterState
    from ..common.module_error import ModuleError
except (ImportError, ValueError):
    from helpermodules import log
    from modules.common import modbus
    from modules.common.abstract_component import AbstractCounter
    from modules.common.component_state import CounterState
    from modules.common.module_error import ModuleError


def get_default_config() -> dict:
    return {
        "name": "Alpha ESS Zähler",
        "id": 0,
        "type": "counter",
        "configuration":
        {
            "version": 1
        }
    }


class AlphaEssCounter(AbstractCounter):
    def __init__(self, device_id: int, component_config: dict, tcp_client: modbus.ModbusClient) -> None:
        try:
            super().__init__(device_id, component_config, tcp_client)
        except Exception as e:
            self.process_error(e)

    def get_values(self) -> CounterState:
        log.MainLogger().debug(
            "Komponente "+self.data["config"]["name"]+" auslesen.")
        time.sleep(0.1)
        factory_method = self.__get_values_factory(
            self.data["config"]["configuration"]["version"])
        return factory_method(unit=85)

    def __get_values_factory(self, version: int) -> Callable[[int], Tuple[int, int, int, List[int]]]:
        return self.__get_values_before_v123 if version == 0 else self.__get_values_since_v123

    def __get_values_before_v123(self, unit: int) -> CounterState:
        try:
            power_all = self.client.read_holding_registers(
                0x0006, modbus.ModbusDataType.INT_32, unit=unit)
            exported = self.client.read_holding_registers(
                0x0008, modbus.ModbusDataType.INT_32, unit=unit) * 10
            imported = self.client.read_holding_registers(
                0x000A, modbus.ModbusDataType.INT_32, unit=unit) * 10
            currents = []
            regs = [0x0000, 0x0002, 0x0004]
            for register in regs:
                value = self.client.read_holding_registers(
                    register, modbus.ModbusDataType.INT_32, unit=unit) / 230
                currents.append(value)

            counter_state = CounterState(
                voltages=[0, 0, 0],
                currents=currents,
                powers=[0, 0, 0],
                power_factors=[0, 0, 0],
                imported=imported,
                exported=exported,
                power_all=power_all,
                frequency=50
            )
            return counter_state
        except ModuleError:
            raise
        except Exception as e:
            self.process_error(e)

    def __get_values_since_v123(self, unit: int) -> CounterState:
        try:
            power_all = self.client.read_holding_registers(
                0x0021, modbus.ModbusDataType.INT_32, unit=unit)
            exported = self.client.read_holding_registers(
                0x0010, modbus.ModbusDataType.INT_32, unit=unit) * 10
            imported = self.client.read_holding_registers(
                0x0012, modbus.ModbusDataType.INT_32, unit=unit) * 10
            currents = []
            regs = [0x0017, 0x0018, 0x0019]
            for register in regs:
                value = self.client.read_holding_registers(
                    register, modbus.ModbusDataType.INT_16, unit=unit) / 1000
                currents.append(value)

            counter_state = CounterState(
                voltages=[0, 0, 0],
                currents=currents,
                powers=[0, 0, 0],
                power_factors=[0, 0, 0],
                imported=imported,
                exported=exported,
                power_all=power_all,
                frequency=50
            )
            return counter_state
        except ModuleError:
            raise
        except Exception as e:
            self.process_error(e)
