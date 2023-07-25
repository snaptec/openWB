#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType, Endian
from modules.common.simcount import SimCounter
from modules.common.store import get_counter_value_store
from modules.devices.sungrow.config import SungrowCounterSetup
from modules.devices.sungrow.version import Version


class SungrowCounter:
    def __init__(self,
                 device_id: int,
                 device_modbus_id: int,
                 component_config: Union[Dict, SungrowCounterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.__device_modbus_id = device_modbus_id
        self.component_config = dataclass_from_dict(SungrowCounterSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, pv_power: float):
        unit = self.__device_modbus_id
        if self.component_config.configuration.version == Version.SH:
            power = self.__tcp_client.read_input_registers(13009, ModbusDataType.INT_32,
                                                           wordorder=Endian.Little, unit=unit) * -1
            # no valid data for powers per phase
            # powers = self.__tcp_client.read_input_registers(5084, [ModbusDataType.INT_16] * 3,
            #                                                 wordorder=Endian.Little, unit=unit)
            # powers = [power / 10 for power in powers]
            # log.info("power: " + str(power) + " powers?: " + str(powers))
        else:
            if pv_power != 0:
                power = self.__tcp_client.read_input_registers(5082, ModbusDataType.INT_32,
                                                               wordorder=Endian.Little, unit=unit)
            else:
                power = self.__tcp_client.read_input_registers(5090, ModbusDataType.INT_32,
                                                               wordorder=Endian.Little, unit=unit)

            # no valid data for powers per phase
            # powers = self.__tcp_client.read_input_registers(5084, [ModbusDataType.UINT_16] * 3,
            #                                                 wordorder=Endian.Little, unit=unit)
            # powers = [power / 10 for power in powers]
            # log.info("power: " + str(power) + " powers?: " + str(powers))
        frequency = self.__tcp_client.read_input_registers(5035, ModbusDataType.UINT_16, unit=unit) / 10
        voltages = self.__tcp_client.read_input_registers(5018, [ModbusDataType.UINT_16] * 3,
                                                          wordorder=Endian.Little, unit=unit)
        voltages = [voltage / 10 for voltage in voltages]

        imported, exported = self.sim_counter.sim_count(power)

        counter_state = CounterState(
            imported=imported,
            exported=exported,
            power=power,
            voltages=voltages,
            frequency=frequency
        )
        self.store.set(counter_state)


component_descriptor = ComponentDescriptor(configuration_factory=SungrowCounterSetup)
