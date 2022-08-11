#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.sma_sunny_boy.config import SmaSunnyBoyCounterSetup


class SmaSunnyBoyCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SmaSunnyBoyCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SmaSunnyBoyCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        imp = self.__tcp_client.read_holding_registers(30865, ModbusDataType.UINT_32, unit=3)
        exp = self.__tcp_client.read_holding_registers(30867, ModbusDataType.UINT_32, unit=3)
        if imp > 5:
            power = imp
        else:
            power = exp * -1

        topic_str = "openWB/set/system/device/{}/component/{}/".format(self.__device_id, self.component_config.id)
        imported, exported = self.__sim_count.sim_count(power, topic=topic_str, data=self.simulation, prefix="bezug")

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SmaSunnyBoyCounterSetup)
