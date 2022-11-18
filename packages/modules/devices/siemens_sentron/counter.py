#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.devices.siemens_sentron.config import SiemensSentronCounterSetup


class SiemensSentronCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SiemensSentronCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SiemensSentronCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        with self.__tcp_client:
            imported = self.__tcp_client.read_holding_registers(801, ModbusDataType.FLOAT_64, unit=1)
            exported = self.__tcp_client.read_holding_registers(809, ModbusDataType.FLOAT_64, unit=1)
            power = self.__tcp_client.read_holding_registers(65, ModbusDataType.FLOAT_32, unit=1)
            powers = self.__tcp_client.read_holding_registers(25, [ModbusDataType.FLOAT_32] * 3, unit=1)
            frequency = self.__tcp_client.read_holding_registers(55, ModbusDataType.FLOAT_32, unit=1)
            currents = self.__tcp_client.read_holding_registers(13, [ModbusDataType.FLOAT_32] * 3, unit=1)
            voltages = self.__tcp_client.read_holding_registers(1, [ModbusDataType.FLOAT_32] * 3, unit=1)
            power_factors = self.__tcp_client.read_holding_registers(37, [ModbusDataType.FLOAT_32] * 3, unit=1)

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power,
            powers=powers,
            currents=currents,
            voltages=voltages,
            frequency=frequency,
            power_factors=power_factors
        )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SiemensSentronCounterSetup)
