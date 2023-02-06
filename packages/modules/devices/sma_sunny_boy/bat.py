#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusTcpClient_, ModbusDataType
from modules.common.store import get_bat_value_store
from modules.devices.sma_sunny_boy.config import SmaSunnyBoyBatSetup


class SunnyBoyBat:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SmaSunnyBoyBatSetup],
                 tcp_client: ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SmaSunnyBoyBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def read(self) -> BatState:
        unit = 3
        soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.UINT_32, unit=unit)
        imp = self.__tcp_client.read_holding_registers(31393, ModbusDataType.INT_32, unit=unit)
        exp = self.__tcp_client.read_holding_registers(31395, ModbusDataType.INT_32, unit=unit)
        if imp > 5:
            power = imp
        else:
            power = exp * -1

        exported = self.__tcp_client.read_holding_registers(31401, ModbusDataType.UINT_64, unit=3)
        imported = self.__tcp_client.read_holding_registers(31397, ModbusDataType.UINT_64, unit=3)

        return BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )

    def update(self) -> None:
        self.store.set(self.read())


component_descriptor = ComponentDescriptor(configuration_factory=SmaSunnyBoyBatSetup)
