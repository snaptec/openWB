#!/usr/bin/python3
import logging
from typing import Iterable, List

from pymodbus.constants import Endian

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import InverterState, BatState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_inverter_value_store, get_bat_value_store
from modules.common.simcount import SimCountFactory
from modules.common.store.ramdisk import files

log = logging.getLogger("E3DC Battery")


def update_e3dc_battery(addresses: Iterable[str], read_external: int, pv_other: bool):
    soc = 0
    count = 0
    battery_power = 0
    # pv_external - > pv Leistung die als externe Produktion an e3dc angeschlossen ist
    # nur auslesen wenn als relevant parametrisiert  (read_external = 1) , sonst doppelte Auslesung
    pv_external = 0
    # pv -> pv Leistung die direkt an e3dc angeschlossen ist
    pv = 0
    for address in addresses:
        log.debug("Battery Ip: %s, read_external %d pv_other %s", address, read_external, pv_other)
        count += 1
        with ModbusClient(address, port=502) as client:
            # 40082 SoC
            soc += client.read_holding_registers(40082, ModbusDataType.INT_16, unit=1)
            # 40069 Speicherleistung
            battery_power += client.read_holding_registers(40069,
                                                           ModbusDataType.INT_32, wordorder=Endian.Little, unit=1)
            # 40067 PV Leistung
            pv += (client.read_holding_registers(40067, ModbusDataType.INT_32, wordorder=Endian.Little, unit=1) * -1)
            if read_external == 1:
                # 40075 externe PV Leistung
                pv_external += client.read_holding_registers(40075,
                                                             ModbusDataType.INT_32, wordorder=Endian.Little, unit=1)
    soc = soc / count
    log.debug("Battery soc %d battery_power %d pv %d pv_external %d count ip %d",
              soc, battery_power, pv, pv_external, count)
    counter_import, counter_export = SimCountFactory().get_sim_counter()().sim_count(battery_power, prefix="speicher")
    get_bat_value_store(1).set(BatState(power=battery_power, soc=soc, imported=counter_import, exported=counter_export))
    # pv_other sagt aus, ob WR definiert ist, und dessen PV Leistung auch gilt
    # wenn 0 gilt nur PV und pv_external aus e3dc
    pv_total = pv + pv_external
    # Wenn wr1 nicht definiert ist, gilt nur die PV Leistung die hier im Modul ermittelt wurde
    # als gesamte PV Leistung für wr1
    if not pv_other or pv_total != 0:
        # Wenn wr1 definiert ist, gilt die bestehende PV Leistung aus Wr1 und das was hier im Modul ermittelt wurde
        # als gesamte PV Leistung für wr1
        if pv_other:
            try:
                pv_total = pv_total + files.pv[0].power.read()
            except:
                pass
        log.debug("wr update pv_other %s pv_total %d", pv_other, pv_total)
        _, counter_pv = SimCountFactory().get_sim_counter()().sim_count(pv_total, prefix="pv")
        get_inverter_value_store(1).set(InverterState(counter=counter_pv, power=pv_total))


def update(address1: str, address2: str, read_external: int, pvmodul: str):
    # read_external is 0 or 1
    log.debug("Beginning update")
    addresses = [address for address in [address1, address2] if address != "none"]
    pv_other = pvmodul != "none"
    update_e3dc_battery(addresses, read_external, pv_other)
    log.debug("Update completed successfully")


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
