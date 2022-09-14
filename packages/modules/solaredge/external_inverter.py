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
from modules.solaredge.config import SolaredgeExternalInverterSetup
from modules.solaredge.scale import scale_registers
from modules.solaredge.meter import SolaredgeMeterRegisters

log = logging.getLogger(__name__)


class SolaredgeExternalInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, SolaredgeExternalInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.component_config = dataclass_from_dict(SolaredgeExternalInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.registers = SolaredgeMeterRegisters(self.component_config.configuration.meter_id)
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, state: InverterState) -> None:
        self.__store.set(state)

    def read_state(self) -> InverterState:
        def read_scaled_int16(address: int, count: int):
            return scale_registers(
                self.__tcp_client.read_holding_registers(
                    address,
                    [ModbusDataType.INT_16] * (count + 1),
                    unit=self.component_config.configuration.modbus_id)
            )

        def read_scaled_uint32(address: int, count: int):
            return scale_registers(
                self.__tcp_client.read_holding_registers(
                    address,
                    [ModbusDataType.UINT_32] * count + [ModbusDataType.INT_16],
                    unit=self.component_config.configuration.modbus_id)
            )

        with self.__tcp_client:
            power = read_scaled_int16(self.registers.powers, 4)[0]
            exported = read_scaled_uint32(self.registers.imp_exp, 8)[0]
            currents = read_scaled_int16(self.registers.currents, 3)

        return InverterState(
            exported=exported,
            power=power,
            currents=currents
        )


component_descriptor = ComponentDescriptor(configuration_factory=SolaredgeExternalInverterSetup)
