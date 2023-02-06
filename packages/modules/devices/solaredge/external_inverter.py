#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.store import get_inverter_value_store
from modules.devices.solaredge.config import SolaredgeExternalInverterSetup
from modules.devices.solaredge.scale import create_scaled_reader
from modules.devices.solaredge.meter import SolaredgeMeterRegisters

log = logging.getLogger(__name__)


class SolaredgeExternalInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaredgeExternalInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SolaredgeExternalInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.registers = SolaredgeMeterRegisters(self.component_config.configuration.meter_id)
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self._read_scaled_int16 = create_scaled_reader(
            self.__tcp_client, self.component_config.configuration.modbus_id, ModbusDataType.INT_16
        )
        self._read_scaled_uint32 = create_scaled_reader(
            self.__tcp_client, self.component_config.configuration.modbus_id, ModbusDataType.UINT_32
        )

    def update(self) -> None:
        self.store.set(self.read_state())

    def read_state(self) -> InverterState:
        power = self._read_scaled_int16(self.registers.powers, 4)[0]
        exported = self._read_scaled_uint32(self.registers.imp_exp, 8)[0]
        currents = self._read_scaled_int16(self.registers.currents, 3)

        return InverterState(
            exported=exported,
            power=power,
            currents=currents
        )


component_descriptor = ComponentDescriptor(configuration_factory=SolaredgeExternalInverterSetup)
