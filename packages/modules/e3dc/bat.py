#!/usr/bin/env python3
from typing import Dict, Union
import logging

from dataclass_utils import dataclass_from_dict
from modules.common import modbus
from modules.common.component_state import BatState
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType, Endian
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_bat_value_store
from modules.common.store import get_inverter_value_store
from modules.common.simcount._simcounter import SimCounter
from modules.e3dc.config import e3dcBatSetup
from modules.common.store.ramdisk import files


log = logging.getLogger(__name__)


class e3dcBat:
    def __init__(self,
                 device_id: int,
                 ip_address1: str,
                 ip_address2: str,
                 read_ext: int,
                 pvmodul: str,
                 component_config: Union[Dict, e3dcBatSetup]) -> None:
        self.__device_id = device_id
        self.component_config = dataclass_from_dict(e3dcBatSetup, component_config)
        # bat
        self.__sim_counter = SimCounter(self.__device_id, self.component_config.id, prefix="speicher")
        self.__store = get_bat_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)
        self.__addresses = [address for address in [ip_address1, ip_address2] if address != "none"]
        self.__read_ext = read_ext
        self.__pvmodul = pvmodul
        self.__pvother = pvmodul != "none"

    def update(self) -> None:
        soc = 0
        count = 0
        power = 0
        # pv_external - > pv Leistung
        # die als externe Produktion an e3dc angeschlossen ist
        # nur auslesen wenn als relevant parametrisiert
        # (read_external = 1) , sonst doppelte Auslesung
        pv_external = 0
        # pv -> pv Leistung die direkt an e3dc angeschlossen ist
        pv = 0
        for address in self.__addresses:
            log.debug("Ip: %s, read_ext %d pv_other %s", address,
                      self.__read_ext, self.__pvother)
            count += 1
            with modbus.ModbusTcpClient_(address, 502) as client:
                # 40082 SoC
                soc += client.read_holding_registers(40082, ModbusDataType.INT_16, unit=1)
                # 40069 Speicherleistung
                power += client.read_holding_registers(40069, ModbusDataType.INT_32, wordorder=Endian.Little, unit=1)
                # 40067 PV Leistung
                pv += (client.read_holding_registers(40067,
                       ModbusDataType.INT_32, wordorder=Endian.Little,
                       unit=1) * -1)
                if self.__read_ext == 1:
                    # 40075 externe PV Leistung
                    pv_external += client.read_holding_registers(40075, ModbusDataType.INT_32,
                                                                 wordorder=Endian.Little, unit=1)
        soc = soc / count
        log.debug("soc %d power %d pv %d pv_external %d c ip %d",
                  soc, power, pv, pv_external, count)
        imported, exported = self.__sim_counter.sim_count(power)
        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
        # pv_other sagt aus, ob WR definiert ist,
        # und dessen PV Leistung auch gilt
        # wenn 0 gilt nur PV und pv_external aus e3dc
        pv_total = pv + pv_external
        # Wenn wr1 nicht definiert ist,
        # gilt nur die PV Leistung die hier im Modul ermittelt wurde
        # als gesamte PV Leistung für wr1
        if not self.__pvother or pv_total != 0:
            # Wenn wr1 definiert ist, gilt die bestehende PV Leistung
            # aus Wr1 und das was hier im Modul ermittelt wurde
            # als gesamte PV Leistung für wr1
            if self.__pvother:
                try:
                    pv_total = pv_total + files.pv[0].power.read()
                except Exception:
                    pass
            log.debug("wr update pv_other %s pv_total %d",
                      self.__pvother, pv_total)
            # pv
            self.__sim_counterpv = SimCounter(self.__device_id, self.component_config.id, prefix="pv")
            self.__storepv = get_inverter_value_store(self.component_config.id)
            _, exportedpv = self.__sim_counterpv.sim_count(pv_total)
            inverter_state = InverterState(
                power=pv_total,
                exported=exportedpv
            )
            self.__storepv.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=e3dcBatSetup)
