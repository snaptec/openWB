#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.sungrow.config import SungrowBatSetup


class SungrowBat:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SungrowBatSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SungrowBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        unit = 1
        with self.__tcp_client:
            soc = int(self.__tcp_client.read_input_registers(13022, ModbusDataType.INT_16, unit=unit) / 10)
            resp = self.__tcp_client.delegate.read_input_registers(13000, 1, unit=unit)
            binary = bin(resp.registers[0])[2:].zfill(8)
            power = self.__tcp_client.read_input_registers(13021, ModbusDataType.INT_16, unit=unit)
            if binary[5] == "1":
                power = power * -1

        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config.id)+"/"
        imported, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.simulation, prefix="speicher"
        )
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=SungrowBatSetup)
