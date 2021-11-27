#!/usr/bin/env python3

from typing import List, Tuple

from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.common.modbus import ModbusDataType


class Lovato:
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
            return [val / 100 for val in self.client.read_input_registers(
                0x0001, [ModbusDataType.INT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_input_registers(0x0048, ModbusDataType.FLOAT_32, unit=self.id) * 1000
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = [val / 100 for val in self.client.read_input_registers(
                0x0013, [ModbusDataType.INT_32]*3, unit=self.id
            )]
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
            return [val / 10000 for val in self.client.read_input_registers(
                0x0025, [ModbusDataType.INT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            frequency = self.client.read_input_registers(0x0031, ModbusDataType.INT_32, unit=self.id) / 100
            if frequency > 100:
                frequency = frequency / 10
            return frequency
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return [val / 10000 for val in self.client.read_input_registers(
                0x0007, [ModbusDataType.INT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            finalbezug1 = self.client.read_input_registers(0x1a1f, ModbusDataType.INT_32, unit=self.id)
            finalbezug2 = self.client.read_input_registers(0x1a21, ModbusDataType.INT_32, unit=self.id)
            return max(finalbezug1, finalbezug2)
        except Exception as e:
            self.__process_error(e)
