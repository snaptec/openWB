#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.solaredge.config import SolaredgeExternalInverterSetup


class SolaredgeExternalInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaredgeExternalInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(SolaredgeExternalInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, state: InverterState) -> None:
        self.__store.set(state)

    def read_state(self) -> InverterState:
        unit = self.component_config.configuration.modbus_id
        # 40380 = "Meter 2/Total Real Power (sum of active phases)" (Watt)
        power = self.__tcp_client.read_holding_registers(40380, ModbusDataType.INT_16, unit=unit)
        topic_str = "openWB/set/system/device/" + str(self.__device_id) + \
            "/component/" + str(self.component_config.id)+"/"
        _, exported = self.__sim_count.sim_count(power, topic=topic_str, data=self.simulation, prefix="pv")

        return InverterState(
            exported=exported,
            power=power
        )


component_descriptor = ComponentDescriptor(configuration_factory=SolaredgeExternalInverterSetup)
