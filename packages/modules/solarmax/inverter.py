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
from modules.solarmax.config import SolarmaxInverterSetup


class SolarmaxInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolarmaxInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_,
                 modbus_id: int) -> None:
        self.__device_id = device_id
        self.__modbus_id = modbus_id
        self.component_config = dataclass_from_dict(SolarmaxInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        with self.__tcp_client:
            power = self.__tcp_client.read_holding_registers(4151, ModbusDataType.UINT_32, unit=self.__modbus_id) * -1
        power = power / 10
        topic_str = "openWB/set/system/device/" + \
            str(self.__device_id)+"/component/" + \
            str(self.component_config.id)+"/"
        _, exported = self.__sim_count.sim_count(power,
                                                 topic=topic_str,
                                                 data=self.simulation,
                                                 prefix="pv%s" % ("" if self.component_config.id == 1 else "2"))
        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SolarmaxInverterSetup)
