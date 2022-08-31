#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.solaredge.config import SolaredgeInverterSetup
from modules.solaredge.scale import scale_registers


class SolaredgeInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaredgeInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SolaredgeInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, state: InverterState) -> None:
        self.__store.set(state)

    def read_state(self):
        def read_scaled_int16(address: int, count: int):
            return scale_registers(
                self.__tcp_client.read_holding_registers(
                    address,
                    [ModbusDataType.INT_16] * (count+1),
                    unit=self.component_config.configuration.modbus_id)
            )

        def read_scaled_uint16(address: int, count: int):
            return scale_registers(
                self.__tcp_client.read_holding_registers(
                    address,
                    [ModbusDataType.UINT_16] * (count)+[ModbusDataType.INT_16],
                    unit=self.component_config.configuration.modbus_id)
            )

        def read_scaled_uint32(address: int, count: int):
            return scale_registers(
                self.__tcp_client.read_holding_registers(
                    address,
                    [ModbusDataType.UINT_32] * (count)+[ModbusDataType.INT_16],
                    unit=self.component_config.configuration.modbus_id)
            )
        # 40083 = AC Power value (Watt)
        # 40084 = AC Power scale factor
        power = read_scaled_int16(40083, 1)[0] * -1

        # 40093 = AC Lifetime Energy production (Watt hours)
        # 40095 = AC Lifetime scale factor
        exported = read_scaled_uint32(40093, 1)[0]
        # 40072/40073/40074 = AC Phase A/B/C Current value (Amps)
        # 40075 = AC Current scale factor
        currents = read_scaled_uint16(40072, 3)

        return InverterState(
            power=power,
            exported=exported,
            currents=currents
        )


component_descriptor = ComponentDescriptor(configuration_factory=SolaredgeInverterSetup)
