#!/usr/bin/env python3
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.devices.solaredge.config import SolaredgeInverterSetup
from modules.devices.solaredge.scale import create_scaled_reader


class SolaredgeInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaredgeInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SolaredgeInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self._read_scaled_int16 = create_scaled_reader(
            self.__tcp_client, self.component_config.configuration.modbus_id, ModbusDataType.INT_16
        )
        self._read_scaled_uint16 = create_scaled_reader(
            self.__tcp_client, self.component_config.configuration.modbus_id, ModbusDataType.UINT_16
        )
        self._read_scaled_uint32 = create_scaled_reader(
            self.__tcp_client, self.component_config.configuration.modbus_id, ModbusDataType.UINT_32
        )

    def update(self) -> None:
        self.store.set(self.read_state())

    def read_state(self):
        # 40083 = AC Power value (Watt)
        # 40084 = AC Power scale factor
        power = self._read_scaled_int16(40083, 1)[0] * -1

        # 40093 = AC Lifetime Energy production (Watt hours)
        # 40095 = AC Lifetime scale factor
        exported = self._read_scaled_uint32(40093, 1)[0]
        # 40072/40073/40074 = AC Phase A/B/C Current value (Amps)
        # 40075 = AC Current scale factor
        currents = self._read_scaled_uint16(40072, 3)
        # 40100 = DC Power value (Watt)
        # 40101 = DC Power scale factor
        dc_power = self._read_scaled_int16(40100, 1)[0] * -1

        return InverterState(
            power=power,
            exported=exported,
            currents=currents,
            dc_power=dc_power
        )


component_descriptor = ComponentDescriptor(configuration_factory=SolaredgeInverterSetup)
