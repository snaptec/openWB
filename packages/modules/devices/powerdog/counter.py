#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.powerdog.config import PowerdogCounterSetup

log = logging.getLogger(__name__)


class PowerdogCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, PowerdogCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(PowerdogCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self):
        with self.__tcp_client:
            home_consumption = self.__tcp_client.read_input_registers(40026, ModbusDataType.INT_32, unit=1)
        log.debug("Powerdog Hausverbrauch[W]: " + str(home_consumption))
        return home_consumption

    def set_counter_state(self, power: float) -> None:
        imported, exported = self.sim_counter.sim_count(power)
        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=PowerdogCounterSetup)
