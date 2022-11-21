#!/usr/bin/env python3
from typing import Dict, Union

from pymodbus.constants import Endian

from dataclass_utils import dataclass_from_dict
from modules.devices.carlo_gavazzi.config import CarloGavazziCounterSetup
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store


class CarloGavazziCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, CarloGavazziCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(CarloGavazziCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        unit = 1
        with self.__tcp_client:
            voltages = [val / 10 for val in self.__tcp_client.read_input_registers(
                0x00, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little, unit=unit)]
            powers = [val / 10 for val in self.__tcp_client.read_input_registers(
                0x12, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little, unit=unit)]
            power = sum(powers)
            currents = [(val / 1000) for val in self.__tcp_client.read_input_registers(
                0x0C, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little, unit=unit)]
            frequency = self.__tcp_client.read_input_registers(0x33, ModbusDataType.INT_16, unit=unit) / 10
            if frequency > 100:
                frequency = frequency / 10

        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            imported=imported,
            exported=exported,
            power=power,
            frequency=frequency
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=CarloGavazziCounterSetup)
