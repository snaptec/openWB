#!/usr/bin/env python3
from typing import Dict, Union
from pymodbus.constants import Endian

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.devices.solax.config import SolaxInverterSetup


class SolaxInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaxInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_,
                 modbus_id: int) -> None:
        self.component_config = dataclass_from_dict(SolaxInverterSetup, component_config)
        self.__modbus_id = modbus_id
        self.__tcp_client = tcp_client
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        with self.__tcp_client:
            power_temp = self.__tcp_client.read_input_registers(10, [ModbusDataType.UINT_16] * 2, unit=self.__modbus_id)
            power = sum(power_temp) * -1
            exported = self.__tcp_client.read_input_registers(82, ModbusDataType.UINT_32, wordorder=Endian.Little,
                                                              unit=self.__modbus_id) * 100

        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SolaxInverterSetup)
