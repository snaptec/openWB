#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common import simcount
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.powerdog.config import PowerdogCounterSetup

log = logging.getLogger(__name__)


class PowerdogCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, PowerdogCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(PowerdogCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self):
        with self.__tcp_client:
            home_consumption = self.__tcp_client.read_input_registers(40026, ModbusDataType.INT_32, unit=1)
        log.debug("Powerdog Hausverbrauch[W]: " + str(home_consumption))
        return home_consumption

    def set_counter_state(self, power: float) -> None:
        topic_str = "openWB/set/system/device/{}/component/{}/".format(
            self.__device_id, self.component_config.id
        )
        imported, exported = self.__sim_count.sim_count(
            power,
            topic=topic_str,
            data=self.simulation,
            prefix="bezug"
        )
        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.__store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=PowerdogCounterSetup)
