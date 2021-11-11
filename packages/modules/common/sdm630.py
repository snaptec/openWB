#!/usr/bin/env python3
from typing import List, Tuple

try:
    from ..common import modbus
    from ..common.module_error import ModuleError, ModuleErrorLevel
except (ImportError, ValueError):
    # for 1.9 compatibility
    from modules.common import modbus
    from modules.common.module_error import ModuleError, ModuleErrorLevel


class Sdm630:
    def __init__(self, modbus_id: int, client: modbus.ModbusClient) -> None:
        self.client = client
        self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, ModuleError):
            raise
        else:
            raise ModuleError(__name__+" "+str(type(e))+" "+str(e), ModuleErrorLevel.ERROR) from e

    def get_voltage(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x00, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id)
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_input_registers(0x0048, modbus.ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = self.client.read_input_registers(0x0C, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id)
            power_all = sum(power_per_phase)
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_input_registers(0x004a, modbus.ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x1E, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id)
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            frequency = self.client.read_input_registers(0x46, modbus.ModbusDataType.FLOAT_32, unit=self.id)
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x06, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id)
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            return self.client.read_input_registers(0x0156, modbus.ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)
