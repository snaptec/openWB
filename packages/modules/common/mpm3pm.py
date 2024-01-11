#!/usr/bin/env python3
from typing import List, Tuple

from modules.common import modbus
from modules.common.abstract_counter import AbstractCounter
from modules.common.modbus import ModbusDataType


class Mpm3pm(AbstractCounter):
    def __init__(self, modbus_id: int, client: modbus.ModbusTcpClient_) -> None:
        self.client = client
        self.id = modbus_id

    def get_voltages(self) -> List[float]:
        return [val / 10 for val in self.client.read_input_registers(
            0x08, [ModbusDataType.UINT_32]*3, unit=self.id)]

    def get_imported(self) -> float:
        # Faktorisierung anders als in der Dokumentation angegeben
        return self.client.read_input_registers(0x0002, ModbusDataType.UINT_32, unit=self.id) * 10

    def get_power(self) -> Tuple[List[float], float]:
        powers = [val / 100 for val in self.client.read_input_registers(
            0x14, [ModbusDataType.INT_32]*3, unit=self.id)]
        power = self.client.read_input_registers(0x26, ModbusDataType.INT_32, unit=self.id) / 100
        return powers, power

    def get_exported(self) -> float:
        # Faktorisierung anders als in der Dokumentation angegeben
        return self.client.read_input_registers(0x0004, ModbusDataType.UINT_32, unit=self.id) * 10

    def get_power_factors(self) -> List[float]:
        # Faktorisierung anders als in der Dokumentation angegeben
        return [val / 10 for val in self.client.read_input_registers(
            0x20, [ModbusDataType.UINT_32]*3, unit=self.id)]

    def get_frequency(self) -> float:
        return self.client.read_input_registers(0x2c, ModbusDataType.UINT_32, unit=self.id) / 100

    def get_currents(self) -> List[float]:
        return [val / 100 for val in self.client.read_input_registers(
            0x0E, [ModbusDataType.UINT_32]*3, unit=self.id)]
