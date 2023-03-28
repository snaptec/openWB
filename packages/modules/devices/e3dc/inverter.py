#!/usr/bin/env python3
import logging

from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType, Endian
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.common.simcount._simcounter import SimCounter
from modules.devices.e3dc.config import E3dcInverterSetup


log = logging.getLogger(__name__)


def read_inverter(client: modbus.ModbusTcpClient_) -> int:
    # 40067 PV Leistung
    pv = int(client.read_holding_registers(40067, ModbusDataType.INT_32, wordorder=Endian.Little, unit=1) * -1)
    return pv


class E3dcInverter:
    def __init__(self,
                 device_id: int,
                 component_config: E3dcInverterSetup) -> None:
        self.component_config = component_config
        self.sim_counter = SimCounter(device_id, self.component_config.id, prefix="pv")
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, client: modbus.ModbusTcpClient_) -> None:

        pv = read_inverter(client)
        # Im gegensatz zur Implementierung in Version 1.9 wird nicht mehr die PV
        # Leistung vom WR1 gelesen, da die durch v2.0 separat gehandelt wird
        _, pv_exported = self.sim_counter.sim_count(pv)
        inverter_state = InverterState(
            power=pv,
            exported=pv_exported
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=E3dcInverterSetup)
