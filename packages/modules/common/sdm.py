#!/usr/bin/env python3
from typing import List, Tuple

from modules.common import modbus
from modules.common.abstract_counter import AbstractCounter
from modules.common.modbus import ModbusDataType


class Sdm(AbstractCounter):
    def __init__(self, modbus_id: int, client: modbus.ModbusTcpClient_) -> None:
        self.client = client
        self.id = modbus_id

    def get_imported(self) -> float:
        return self.client.read_input_registers(0x0048, ModbusDataType.FLOAT_32, unit=self.id) * 1000

    def get_exported(self) -> float:
        return self.client.read_input_registers(0x004a, ModbusDataType.FLOAT_32, unit=self.id) * 1000

    def get_frequency(self) -> float:
        frequency = self.client.read_input_registers(0x46, ModbusDataType.FLOAT_32, unit=self.id)
        if frequency > 100:
            frequency = frequency / 10
        return frequency


class Sdm630(Sdm):
    def __init__(self, modbus_id: int, client: modbus.ModbusTcpClient_) -> None:
        super().__init__(modbus_id, client)

    def get_currents(self) -> List[float]:
        return self.client.read_input_registers(0x06, [ModbusDataType.FLOAT_32]*3, unit=self.id)

    def get_power_factors(self) -> List[float]:
        return self.client.read_input_registers(0x1E, [ModbusDataType.FLOAT_32]*3, unit=self.id)

    def get_power(self) -> Tuple[List[float], float]:
        powers = self.client.read_input_registers(0x0C, [ModbusDataType.FLOAT_32]*3, unit=self.id)
        power = sum(powers)
        return powers, power

    def get_voltages(self) -> List[float]:
        return self.client.read_input_registers(0x00, [ModbusDataType.FLOAT_32]*3, unit=self.id)


class Sdm120(Sdm):
    def __init__(self, modbus_id: int, client: modbus.ModbusTcpClient_) -> None:
        super().__init__(modbus_id, client)

    def get_power(self) -> Tuple[List[float], float]:
        power = self.client.read_input_registers(0x0C, ModbusDataType.FLOAT_32, unit=self.id)
        return [power, 0, 0], power

    def get_currents(self) -> List[float]:
        return [self.client.read_input_registers(0x06, ModbusDataType.FLOAT_32, unit=self.id), 0, 0]
