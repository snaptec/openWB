#!/usr/bin/env python3
from typing import Dict, Union
from pymodbus.constants import Endian

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.devices.solax.config import SolaxCounterSetup


class SolaxCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaxCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_,
                 modbus_id: int) -> None:

        self.component_config = dataclass_from_dict(SolaxCounterSetup, component_config)
        self.__modbus_id = modbus_id
        self.__tcp_client = tcp_client
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        with self.__tcp_client:
            power = self.__tcp_client.read_input_registers(70, ModbusDataType.INT_32, wordorder=Endian.Little,
                                                           unit=self.__modbus_id) * -1
            frequency = self.__tcp_client.read_input_registers(7, ModbusDataType.UINT_16, unit=self.__modbus_id) / 100
            try:
                powers = [-value for value in self.__tcp_client.read_input_registers(
                    130, [ModbusDataType.INT_32] * 3, wordorder=Endian.Little, unit=self.__modbus_id
                )]
            except Exception:
                powers = None
            exported, imported = [value * 10
                                  for value in self.__tcp_client.read_input_registers(
                                      72, [ModbusDataType.UINT_32] * 2, wordorder=Endian.Little, unit=self.__modbus_id
                                  )]

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power,
            powers=powers,
            frequency=frequency
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SolaxCounterSetup)
