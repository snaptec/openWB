#!/usr/bin/env python3
import time
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.huawei.config import HuaweiBatSetup


class HuaweiBat:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, HuaweiBatSetup],
                 tcp_client: modbus.ModbusTcpClient_,
                 modbus_id: int) -> None:
        self.__device_id = device_id
        self.__modbus_id = modbus_id
        self.component_config = dataclass_from_dict(HuaweiBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        time.sleep(0.1)
        power = self.__tcp_client.read_holding_registers(37765, ModbusDataType.INT_32, unit=self.__modbus_id)
        time.sleep(0.1)
        soc = self.__tcp_client.read_holding_registers(37760, ModbusDataType.INT_16, unit=self.__modbus_id) / 10

        imported, exported = self.sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=HuaweiBatSetup)
