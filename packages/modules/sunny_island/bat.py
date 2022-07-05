#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.sunny_island.config import SunnyIslandBatSetup


class SunnyIslandBat:
    def __init__(self,
                 component_config: Union[Dict, SunnyIslandBatSetup],
                 tcp_client: modbus.ModbusClient) -> None:
        self.component_config = dataclass_from_dict(SunnyIslandBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        unit = 3
        with self.__tcp_client:
            soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.INT_32, unit=unit)
            power = self.__tcp_client.read_holding_registers(30775, ModbusDataType.INT_32, unit=unit) * -1
            [imported, exported] = self.__tcp_client.read_holding_registers(30595, [ModbusDataType.INT_32]*2, unit=unit)

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=SunnyIslandBatSetup)
