#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.sungrow.config import SungrowBatSetup


class SungrowBat:
    def __init__(self,
                 device_id: int,
                 device_modbus_id: int,
                 component_config: Union[Dict, SungrowBatSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.__device_modbus_id = device_modbus_id
        self.component_config = dataclass_from_dict(SungrowBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        unit = self.__device_modbus_id
        soc = int(self.__tcp_client.read_input_registers(13022, ModbusDataType.INT_16, unit=unit) / 10)
        resp = self.__tcp_client.delegate.read_input_registers(13000, 1, unit=unit)
        binary = bin(resp.registers[0])[2:].zfill(8)
        power = self.__tcp_client.read_input_registers(13021, ModbusDataType.INT_16, unit=unit)
        if binary[5] == "1":
            power = power * -1

        imported, exported = self.sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=SungrowBatSetup)
