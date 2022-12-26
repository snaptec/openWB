#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusTcpClient_, ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store
from modules.devices.sma_sunny_boy.config import SmaSunnyBoySmartEnergyBatSetup


class SunnyBoySmartEnergyBat:
    SMA_INT32_NAN = 0xFFFFFFFF  # SMA uses this value to represent NaN

    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SmaSunnyBoySmartEnergyBatSetup],
                 tcp_client: ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SmaSunnyBoySmartEnergyBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        self.store.set(self.read())

    def read(self) -> BatState:
        unit = 3
        soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.UINT_32, unit=unit)
        current = self.__tcp_client.read_holding_registers(30843, ModbusDataType.INT_32, unit=unit)/-1000
        voltage = self.__tcp_client.read_holding_registers(30851, ModbusDataType.INT_32, unit=unit)/100

        if soc == self.SMA_INT32_NAN:
            # If the storage is empty and nothing is produced on the DC side, the inverter does not supply any values.
            soc = 0
            power = 0
        else:
            power = current*voltage
        imported, exported = self.sim_counter.sim_count(power)

        return BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )


component_descriptor = ComponentDescriptor(configuration_factory=SmaSunnyBoySmartEnergyBatSetup)
