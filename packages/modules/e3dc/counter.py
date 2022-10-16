#!/usr/bin/env python3
import logging
import os
from typing import Dict, Union

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import CounterState
from modules.common.component_type import ComponentDescriptor
from modules.common.fault_state import ComponentInfo
from modules.common.simcount._simcounter import SimCounter
from modules.common.modbus import ModbusDataType, Endian
from modules.common.store import get_counter_value_store
from modules.e3dc.config import e3dcCounterSetup

log = logging.getLogger(__name__)


class e3dcCounter:
    def __init__(self,
                 device_id: int,
                 ip_address1: str,
                 ip_address2: str,
                 read_ext: int,
                 pvmodul: str,
                 component_config: Union[Dict, e3dcCounterSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(e3dcCounterSetup, component_config)
        self.__sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="bezug")
        self.__store = get_counter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self.__ip_address1 = ip_address1

    def update(self):
        log.debug("Beginning EVU update")
        file_adr = '/var/www/html/openWB/ramdisk/e3dc_evu_addr.'
        file_adr += str(self.__ip_address1)
        adr = 0
        if os.path.isfile(file_adr):
            with open(file_adr, 'r') as f:
                adr = int(f.read())
        with modbus.ModbusTcpClient_(self.__ip_address1, 502) as client:
            # 40074 EVU Punkt negativ -> Einspeisung in Watt
            power = client.read_holding_registers(40073, ModbusDataType.INT_32, wordorder=Endian.Little, unit=1)
            # 40130 Phasenleistung in Watt
            # max 6 Leistungsmesser verbaut ab 410105, typ 1 ist evu
            # bei den meisten e3dc auf 40128
            # for i in range (40104,40132,4):
            if (adr == 0):
                for i in range(40128, 40103, -4):
                    powers = client.read_holding_registers(i, [ModbusDataType.INT_16] * 4, unit=1)
                    log.debug("I: %d, p0 %d p1 a1 %d p2 a2 %d p3 a3 %d",
                              i, powers[0], powers[1], powers[2], powers[3])
                    if powers[0] == 1:
                        log.debug("Evu Leistungsmessung gefunden, save %d", i)
                        with open(file_adr, 'w') as f:
                            f.write(str(i))
                        break
            else:
                powers = client.read_holding_registers(adr, [ModbusDataType.INT_16] * 4, unit=1)
                log.debug("adr: %d, p0 %d p1 a1 %d p2 a2 %d p3 a3 %d",
                          adr, powers[0], powers[1], powers[2], powers[3])
        imported, exported = self.__sim_counter.sim_count(power)
        counter_state = CounterState(
            imported=imported,
            exported=exported,
            powers=powers[1:],
            power=power
        )
        self.__store.set(counter_state)
        log.debug("Update completed successfully")


component_descriptor = ComponentDescriptor(configuration_factory=e3dcCounterSetup)
