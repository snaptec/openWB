#!/usr/bin/env python3
import time
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.huawei.config import HuaweiCounterSetup


class HuaweiCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, HuaweiCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_,
                 modbus_id: int) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(HuaweiCounterSetup, component_config)
        self.__modbus_id = modbus_id
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        time.sleep(0.1)
        power = self.__tcp_client.read_holding_registers(37113, ModbusDataType.INT_32, unit=self.__modbus_id) * -1
        time.sleep(0.1)
        currents = [val / -100 for val in self.__tcp_client.read_holding_registers(
            37107, [ModbusDataType.INT_32] * 3, unit=self.__modbus_id)]

        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            currents=currents,
            imported=imported,
            exported=exported,
            power=power
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=HuaweiCounterSetup)
