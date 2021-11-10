#!/usr/bin/env python3

from typing import List, Tuple

try:
    from ..common import modbus
    from ...helpermodules import log
    from ..common.module_error import ModuleError, ModuleErrorLevels
except:
    # for 1.9 compability
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from helpermodules import log
    from modules.common import modbus
    from modules.common.module_error import ModuleError, ModuleErrorLevels


class Lovato:
    def __init__(self, modbus_id: int, client: modbus.ModbusClient) -> None:
        self.client = client
        unit=self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, ModuleError):
            raise
        else:
            raise ModuleError(__name__+" "+str(type(e))+" "+str(e), ModuleErrorLevels.ERROR) from e

    def get_voltage(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x0001, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 100
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_input_registers(0x0048, modbus.ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = self.client.read_input_registers(0x0013, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 100
            power_all = self.client.read_input_registers(0x000C, modbus.ModbusDataType.FLOAT_32, unit=self.id)
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
            return self.client.read_input_registers(0x0025,[ modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 10000
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            frequency = self.client.read_input_registers(0x0031, modbus.ModbusDataType.FLOAT_32, unit=self.id) / 100
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x0007, [modbus.ModbusDataType.FLOAT_32]*3, unit=self.id) / 10000
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            finalbezug1 = self.client.read_input_registers(0x1a1f, modbus.ModbusDataType.FLOAT_32, unit=self.id)
            finalbezug2 = self.client.read_input_registers(0x1a21, modbus.ModbusDataType.FLOAT_32, unit=self.id)
            return max(finalbezug1, finalbezug2)
        except Exception as e:
            self.__process_error(e)
