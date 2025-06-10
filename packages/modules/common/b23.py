#!/usr/bin/env python3
from typing import List, Tuple

from modules.common import modbus
from modules.common.abstract_counter import AbstractCounter
from modules.common.modbus import ModbusDataType


class B23(AbstractCounter):
    def __init__(self, modbus_id: int, client: modbus.ModbusTcpClient_) -> None:
        self.client = client
        self.id = modbus_id

    def get_currents(self) -> List[float]:
        return [val / 100 for val in self.client.read_holding_registers(
            0x5B0C, [ModbusDataType.UINT_32]*3, unit=self.id)]

    def get_frequency(self) -> float:
        return self.client.read_holding_registers(0x5B2C, ModbusDataType.UINT_16, unit=self.id) / 100

    def get_imported(self) -> float:
        return self.client.read_holding_registers(0x5000, ModbusDataType.UINT_64, unit=self.id) * 10

    def get_power(self) -> Tuple[List[float], float]:
        # reading of total power and power per phase in one call
        powers = [val / 100 for val in self.client.read_holding_registers(
            0x5B14, [ModbusDataType.INT_32]*4, unit=self.id)]
        return powers[1:4], powers[0]

    def get_power_factors(self) -> List[float]:
        return [val / 1000 for val in self.client.read_holding_registers(
            0x5B3B, [ModbusDataType.INT_16]*3, unit=self.id)]

    def get_voltages(self) -> List[float]:
        return [val / 10 for val in self.client.read_holding_registers(
            0x5B00, [ModbusDataType.UINT_32]*3, unit=self.id)]
