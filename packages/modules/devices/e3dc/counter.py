#!/usr/bin/env python3
import logging
from typing import Tuple, List

from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount._simcounter import SimCounter
from modules.common.modbus import ModbusDataType, Endian
from modules.common.store import get_counter_value_store
from modules.devices.e3dc.config import E3dcCounterSetup

log = logging.getLogger(__name__)


def read_counter(client: modbus.ModbusTcpClient_) -> Tuple[int, List[int]]:
    log.debug("Beginning EVU update")
    power = client.read_holding_registers(40073, ModbusDataType.INT_32, wordorder=Endian.Little, unit=1)
    # 40130,40131, 40132 je Phasenleistung in Watt
    # max 7 Leistungsmesser verbaut ab 40105, typ 1 ist evu
    # Modbus dokumentation Leistungsmesser von #0 bis #6
    # bei den meisten e3dc auf 40128
    meters = client.read_holding_registers(40104, [ModbusDataType.INT_16] * 28, unit=1)
    log.debug("power: %d, meters: %s", power, meters)
    powers = next(meters[i+1:i+4] for i in reversed(range(0, len(meters), 4)) if meters[i] == 1)
    log.debug("powers %s", powers)
    return power, powers


class E3dcCounter:
    def __init__(self,
                 device_id: int,
                 component_config: E3dcCounterSetup) -> None:
        self.component_config = component_config
        self.sim_counter = SimCounter(device_id, self.component_config.id, prefix="bezug")
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, client: modbus.ModbusTcpClient_):
        power, powers = read_counter(client)
        imported, exported = self.sim_counter.sim_count(power)
        counter_state = CounterState(
            imported=imported,
            exported=exported,
            powers=powers,
            power=power
        )
        self.__store.set(counter_state)
        log.debug("Update completed successfully")


component_descriptor = ComponentDescriptor(configuration_factory=E3dcCounterSetup)
