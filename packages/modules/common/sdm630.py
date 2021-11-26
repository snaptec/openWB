#!/usr/bin/env python3
from typing import List, Tuple

from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.common.modbus import ModbusDataType


class Sdm630:
    def __init__(self, modbus_id: int, client: modbus.ModbusClient) -> None:
        self.client = client
        self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, FaultState):
            raise
        else:
            raise FaultState.error(__name__+" "+str(type(e))+" "+str(e)) from e

    def get_voltage(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x00, [ModbusDataType.FLOAT_32]*3, unit=self.id)
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_input_registers(0x0048, ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = self.client.read_input_registers(0x0C, [ModbusDataType.FLOAT_32]*3, unit=self.id)
            power_all = sum(power_per_phase)
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_input_registers(0x004a, ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x1E, [ModbusDataType.FLOAT_32]*3, unit=self.id)
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            frequency = self.client.read_input_registers(0x46, ModbusDataType.FLOAT_32, unit=self.id)
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return self.client.read_input_registers(0x06, [ModbusDataType.FLOAT_32]*3, unit=self.id)
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            return self.client.read_input_registers(0x0156, ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)
