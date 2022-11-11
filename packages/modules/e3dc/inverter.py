#!/usr/bin/env python3
from typing import Tuple
import logging

from modules.common import modbus
from modules.common.component_state import InverterState
from modules.common.component_type import ComponentDescriptor
from modules.common.modbus import ModbusDataType, Endian
from modules.common.fault_state import ComponentInfo
from modules.common.store import get_inverter_value_store
from modules.common.simcount._simcounter import SimCounter
from modules.e3dc.config import E3dcInverterSetup


log = logging.getLogger(__name__)


def read_inverter(client: modbus.ModbusTcpClient_, read_ext) -> Tuple[int, int]:
    # 40067 PV Leistung
    pv = client.read_holding_registers(40067, ModbusDataType.INT_32,
                                       wordorder=Endian.Little, unit=1) * -1
    if read_ext == 1:
        # 40075 externe PV Leistung
        pv_external = client.read_holding_registers(40075, ModbusDataType.INT_32,
                                                    wordorder=Endian.Little, unit=1)
    else:
        pv_external = 0
    return pv, pv_external


class E3dcInverter:
    def __init__(self,
                 device_id: int,
                 component_config: E3dcInverterSetup) -> None:
        self.component_config = component_config
        self.sim_counter = SimCounter(device_id, self.component_config.id, prefix="pv")
        self.__store = get_inverter_value_store(self.component_config.id)
        self.component_info = ComponentInfo.from_component_config(self.component_config)

    def update(self, client: modbus.ModbusTcpClient_) -> None:

        pv, pv_external = read_inverter(client, self.component_config.configuration.read_ext)
        # pv_external - > pv Leistung
        # die als externe Produktion an e3dc angeschlossen ist
        # nur auslesen wenn als relevant parametrisiert
        # (read_external = 1) , sonst doppelte Auslesung
        # pv -> pv Leistung die direkt an e3dc angeschlossen ist
        log.debug("read_ext %d", self.component_config.configuration.read_ext)
        log.debug("pv %d pv_external %d", pv, pv_external)
        # pv_other sagt aus, ob WR definiert ist,
        # und dessen PV Leistung auch gilt
        # wenn 0 gilt nur PV und pv_external aus e3dc
        pv_total = pv + pv_external
        # Wenn wr1 nicht definiert ist,
        # gilt nur die PV Leistung die hier im Modul ermittelt wurde
        # als gesamte PV Leistung für wr1
        # Im gegensatz zu v1.9 implementierung wird nicht mehr die PV
        # leistung vom WR1 gelesen, da die durch v2.0 separat gehandelt wird
        _, pv_exported = self.sim_counter.sim_count(pv_total)
        inverter_state = InverterState(
            power=pv_total,
            exported=pv_exported
        )
        self.__store.set(inverter_state)


component_descriptor = ComponentDescriptor(configuration_factory=E3dcInverterSetup)
