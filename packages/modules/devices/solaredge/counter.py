#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_counter_value_store
from modules.devices.solaredge.config import SolaredgeCounterSetup
from modules.devices.solaredge.scale import create_scaled_reader
from modules.devices.solaredge.meter import SolaredgeMeterRegisters

log = logging.getLogger(__name__)


class SolaredgeCounter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaredgeCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SolaredgeCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.registers = SolaredgeMeterRegisters()
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self._read_scaled_int16 = create_scaled_reader(
            self.__tcp_client, self.component_config.configuration.modbus_id, ModbusDataType.INT_16
        )
        self._read_scaled_uint32 = create_scaled_reader(
            self.__tcp_client, self.component_config.configuration.modbus_id, ModbusDataType.UINT_32
        )

    def update(self):
        powers = [-power for power in self._read_scaled_int16(self.registers.powers, 4)]
        currents = self._read_scaled_int16(self.registers.currents, 3)
        voltages = self._read_scaled_int16(self.registers.voltages, 7)[:3]
        frequency = self._read_scaled_int16(self.registers.frequency, 1)[0]
        power_factors = [power_factor /
                         100 for power_factor in self._read_scaled_int16(self.registers.power_factors, 3)]
        counter_values = self._read_scaled_uint32(self.registers.imp_exp, 8)
        counter_exported, counter_imported = [counter_values[i] for i in [0, 4]]
        counter_state = CounterState(
            imported=counter_imported,
            exported=counter_exported,
            power=powers[0],
            powers=powers[1:],
            voltages=voltages,
            currents=currents,
            power_factors=power_factors,
            frequency=frequency
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SolaredgeCounterSetup)
