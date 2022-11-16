#!/usr/bin/env python3
import logging
import time
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.devices.alpha_ess.config import AlphaEssBatSetup, AlphaEssConfiguration
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusDataType
from modules.common.simcount import SimCounter
from modules.common.store import get_bat_value_store

log = logging.getLogger(__name__)


class AlphaEssBat:
    def __init__(self, device_id: int,
                 component_config: Union[Dict, AlphaEssBatSetup],
                 tcp_client: modbus.ModbusTcpClient_,
                 device_config: AlphaEssConfiguration) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(AlphaEssBatSetup, component_config)
        self.__tcp_client = tcp_client
        self.sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, unit_id: int) -> None:
        # keine Unterschiede zwischen den Versionen

        time.sleep(0.1)
        voltage = self.__tcp_client.read_holding_registers(0x0100, ModbusDataType.INT_16, unit=unit_id)
        time.sleep(0.1)
        current = self.__tcp_client.read_holding_registers(0x0101, ModbusDataType.INT_16, unit=unit_id)

        power = voltage * current * -1 / 100
        log.debug(
            "Alpha Ess Leistung[W]: %f, Speicher-Register: Spannung[V]: %f, Strom[A]: %f" %
            (power, voltage, current)
        )
        time.sleep(0.1)
        soc_reg = self.__tcp_client.read_holding_registers(0x0102, ModbusDataType.INT_16, unit=unit_id)
        soc = int(soc_reg * 0.1)

        imported, exported = self.sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.store.set(bat_state)


component_descriptor = ComponentDescriptor(configuration_factory=AlphaEssBatSetup)
