#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.devices.studer.config import StuderBatSetup


class StuderBat:
    def __init__(self,
                 component_config: Union[Dict, StuderBatSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(StuderBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        unit = 60
        with self.__tcp_client:
            power = self.__tcp_client.read_input_registers(6, ModbusDataType.FLOAT_32, unit=unit)
            imported = self.__tcp_client.read_input_registers(14, ModbusDataType.FLOAT_32, unit=unit) * 48
            exported = self.__tcp_client.read_input_registers(16, ModbusDataType.FLOAT_32, unit=unit) * 48
            soc = self.__tcp_client.read_input_registers(4, ModbusDataType.FLOAT_32, unit=unit)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=StuderBatSetup)
