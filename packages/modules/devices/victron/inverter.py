#!/usr/bin/env python3
import logging
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_inverter_value_store
from modules.devices.victron.config import VictronInverterSetup

log = logging.getLogger(__name__)


class VictronInverter:
    def __init__(self,
                 device_id: int,
                 component_config: Union[Dict, VictronInverterSetup],
                 tcp_client: modbus.ModbusTcpClient_) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(VictronInverterSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
        self.store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self) -> None:
        modbus_id = self.component_config.configuration.modbus_id
        with self.__tcp_client:
            if self.component_config.configuration.mppt:
                try:
                    power = self.__tcp_client.read_holding_registers(789, ModbusDataType.UINT_16, unit=modbus_id) / -10
                except Exception as e:
                    if "GatewayPathUnavailable" in str(e):
                        power = 0
                        log.debug(self.component_config.name +
                                  ": Reg 789 konnte nicht gelesen werden, Power auf 0 gesetzt.")
                    else:
                        raise
            else:
                # Adresse 808-810 ac output connected pv
                # Adresse 811-813 ac input connected pv
                # Adresse 850 mppt Leistung
                power_temp1 = self.__tcp_client.read_holding_registers(808, [ModbusDataType.UINT_16]*6, unit=100)
                power_temp2 = self.__tcp_client.read_holding_registers(850, ModbusDataType.UINT_16, unit=100)
                power = (sum(power_temp1)+power_temp2) * -1

        _, exported = self.sim_counter.sim_count(power)
        inverter_state = InverterState(
            power=power,
            exported=exported
        )
        self.store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=VictronInverterSetup)
