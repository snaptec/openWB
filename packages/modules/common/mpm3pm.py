#!/usr/bin/env python3
from typing import List, Tuple

from modules.common import modbus
from modules.common.fault_state import FaultState
from modules.common.modbus import ModbusDataType


class Mpm3pm:
    def __init__(self, modbus_id: int, client: modbus.ModbusClient) -> None:
        self.client = client
        self.id = modbus_id

    def __process_error(self, e):
        if isinstance(e, FaultState):
            raise
        else:
            raise FaultState.error(__name__+" "+str(type(e))+" " + str(e)) from e

    def get_voltage(self) -> List[float]:
        try:
            return [val / 10 for val in self.client.read_input_registers(
                0x08, [ModbusDataType.FLOAT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_imported(self) -> float:
        try:
            return self.client.read_input_registers(0x0002, ModbusDataType.FLOAT_64, unit=self.id) * 10
        except Exception as e:
            self.__process_error(e)

    def get_power(self) -> Tuple[List[float], float]:
        try:
            power_per_phase = [val / 100 for val in self.client.read_input_registers(
                0x14, [ModbusDataType.FLOAT_32]*3, unit=self.id)]
            power_all = [val / 100 for val in self.client.read_input_registers(
                0x26, ModbusDataType.FLOAT_32, unit=self.id)]
            return power_per_phase, power_all
        except Exception as e:
            self.__process_error(e)

    def get_exported(self) -> float:
        try:
            return self.client.read_input_registers(0x0004, ModbusDataType.FLOAT_64, unit=self.id) * 10
        except Exception as e:
            self.__process_error(e)

    def get_power_factor(self) -> List[float]:
        try:
            return [val / 100 for val in self.client.read_input_registers(
                0x20, [ModbusDataType.FLOAT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_frequency(self) -> float:
        try:
            return self.client.read_input_registers(0x2c, ModbusDataType.FLOAT_64, unit=self.id) / 100
        except Exception as e:
            self.__process_error(e)

    def get_current(self) -> List[float]:
        try:
            return [val / 100 for val in self.client.read_input_registers(
                0x0E, [ModbusDataType.FLOAT_32]*3, unit=self.id)]
        except Exception as e:
            self.__process_error(e)

    def get_counter(self) -> float:
        try:
            return self.client.read_input_registers(0x0004, ModbusDataType.FLOAT_64, unit=self.id) * 10
        except Exception as e:
            self.__process_error(e)
