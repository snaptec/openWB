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
from modules.devices.siemens.config import SiemensBatSetup


class SiemensBat:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SiemensBatSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SiemensBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        with self.__tcp_client:
            power = self.__tcp_client.read_holding_registers(6, ModbusDataType.INT_32, unit=1) * -1
            soc = int(self.__tcp_client.read_holding_registers(8, ModbusDataType.INT_32, unit=1))

        imported, exported = self.sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=SiemensBatSetup)
