#!/usr/bin/env python3
from typing import Dict, Union
from pymodbus.constants import Endian

from dataclass_utils import dataclass_from_dict
from modules.carlo_gavazzi.config import CarloGavazziCounterSetup
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store


class CarloGavazziCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, CarloGavazziCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(CarloGavazziCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
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

        topic_str = "openWB/set/system/device/{}/component/{}/".format(self.__device_id, self.component_config.id)
        imported, exported = self.__sim_count.sim_count(
            power,
            topic=topic_str,
            data=self.simulation,
            prefix="bezug"
        )

        counter_state = CounterState(
            voltages=voltages,
            currents=currents,
            powers=powers,
            imported=imported,
            exported=exported,
            power=power,
            frequency=frequency
        )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=CarloGavazziCounterSetup)
