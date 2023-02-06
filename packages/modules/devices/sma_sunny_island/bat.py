#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_bat_value_store
from modules.devices.sma_sunny_island.config import SmaSunnyIslandBatSetup


class SunnyIslandBat:
    def __init__(self,
                 component_config: Union[Dict, SmaSunnyIslandBatSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SmaSunnyIslandBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def read(self) -> BatState:
        unit = 3
        with self.__tcp_client:
            soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.INT_32, unit=unit)

            power = self.__tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=unit) * -1
            imported, exported = self.__tcp_client.read_holding_registers(30595, [ModbusDataType.INT_32]*2, unit=unit)

        return BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )

    def update(self) -> None:
        self.store.set(self.read())


component_descriptor = ComponentDescriptor(configuration_factory=SmaSunnyIslandBatSetup)
