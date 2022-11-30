#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.sma_sunny_boy.config import SmaSunnyBoyCounterSetup


class SmaSunnyBoyCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SmaSunnyBoyCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SmaSunnyBoyCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        imp = self.__tcp_client.read_holding_registers(30865, ModbusDataType.UINT_32, unit=3)
        exp = self.__tcp_client.read_holding_registers(30867, ModbusDataType.UINT_32, unit=3)
        if imp > 5:
            power = imp
        else:
            power = exp * -1

        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SmaSunnyBoyCounterSetup)
