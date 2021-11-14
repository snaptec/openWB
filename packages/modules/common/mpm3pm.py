#!/usr/bin/env python3
from typing import List, Tuple
try:
    from ..common import modbus
    from ..common.module_error import ModuleError, ModuleErrorLevel
except (ImportError, ValueError):
    # for 1.9 compatibility
    from modules.common import modbus
    from modules.common.module_error import ModuleError, ModuleErrorLevel


class Mpm3pm:
    def __init__(self, modbus_id: int, client: modbus.ModbusClient) -> None:
        self.client = client
        self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, ModuleError):
            raise
        else:
            raise ModuleError(__name__+" "+str(type(e))+" " +
                              str(e), ModuleErrorLevel.ERROR) from e

    def get_voltage(self) -> List[float]:
        try:
            return self.client.read_registers(0x08, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 10
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_input_registers(0x0002, modbus.ModbusDataType.FLOAT_64, unit=self.id) * 10
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = self.client.read_input_registers(
                0x14, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 100
            power_all = self.client.read_input_registers(
                0x26, modbus.ModbusDataType.FLOAT_32, unit=self.id) / 100
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_input_registers(0x0004, modbus.ModbusDataType.FLOAT_64, unit=self.id) * 10
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x20, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 100
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            return self.client.read_input_registers(0x2c, modbus.ModbusDataType.FLOAT_64, unit=self.id) / 100
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return self.client.read_registers(0x0E, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 100
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            return self.client.read_input_registers(0x0004, modbus.ModbusDataType.FLOAT_64, unit=self.id) * 10
        except Exception as e:
            self.__process_error(e)
