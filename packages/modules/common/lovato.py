#!/usr/bin/env python3

from modules.common import modbus
from typing import List, Tuple
from modules.common.abstract_counter import AbstractCounter
from modules.common.modbus import ModbusDataType


class Lovato(AbstractCounter):
    def __init__(self, modbus_id: int, client: modbus.ModbusTcpClient_) -> None:
        self.client = client
        self.id = modbus_id

    def get_voltages(self) -> List[float]:
        return [val / 100 for val in self.client.read_input_registers(
            0x0001, [ModbusDataType.INT_32]*3, unit=self.id)]

    def get_power(self) -> Tuple[List[float], float]:
        powers = [val / 100 for val in self.client.read_input_registers(
            0x0013, [ModbusDataType.INT_32]*3, unit=self.id
        )]
        power = sum(powers)
        return powers, power

    def get_power_factors(self) -> List[float]:
        return [val / 10000 for val in self.client.read_input_registers(
            0x0025, [ModbusDataType.INT_32]*3, unit=self.id)]

    def get_frequency(self) -> float:
        frequency = self.client.read_input_registers(0x0031, ModbusDataType.INT_32, unit=self.id) / 100
        if frequency > 100:
            # needed if external measurement clamps connected
            frequency = frequency / 10
        return frequency

    def get_currents(self) -> List[float]:
        return [val / 10000 for val in self.client.read_input_registers(
            0x0007, [ModbusDataType.INT_32]*3, unit=self.id)]
