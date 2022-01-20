#!/usr/bin/python3
import logging
from statistics import mean
from typing import Iterable

from pymodbus.constants import Endian

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.component_state import InverterState, BatState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_inverter_value_store, get_bat_value_store
from modules.common.simcount import SimCountFactory

log = logging.getLogger("E3DC Battery")

def update_e3dc_battery(address: Iterable[str],external: int,pvother: int,pvwattin: int):
    soc = 0
    count = 0
    speicher = 0
    # extpv - > pv Leistung die als externe Produktion an e3dc angeschlossen ist
    # nur auslesen wenn als relevant parametrisiert  (external = 1) , sonst doppelte Auslesung
    extpv = 0
    # pv -> pv Leistung die direkt an e3dc angeschlossen ist
    pv = 0
    for addr in address:
        log.debug("Battery Ip: %s, external %d pvother %d pvwatt (input) %d", addr,external,pvother,pvwattin)
        if addr != "none":
            count=count+1
            client = ModbusClient(addr, port=502)
            #40082 soc
            soc = soc + client.read_holding_registers(40082,ModbusDataType.INT_16,unit=1)
            #40069 speicherleistung
            speicher = speicher + client.read_holding_registers(40069, ModbusDataType.INT_32, wordorder=Endian.Little,unit=1)
            #40067 pv Leistung
            pv = pv + (client.read_holding_registers(40067, ModbusDataType.INT_32, wordorder=Endian.Little,unit=1) * -1)
            if external == 1:
                #40075 externe pv Leistung
                extpv = extpv + client.read_holding_registers(40075, ModbusDataType.INT_32, wordorder=Endian.Little,unit=1)
    soc = soc / count
    log.debug("Battery soc %d speicherleistung %d pv %d extpv %d anzahl ip %d", soc,speicher,pv,extpv,count)
    cnt= SimCountFactory().get_sim_counter()().sim_count(speicher, prefix="speicher")
    get_bat_value_store(1).set(BatState(power=speicher, soc=soc, imported= cnt[0], exported= cnt[1]))
    # pvother sagt aus, ob wr definiert ist, und dessen pv Leistungs auch gilt
    # wenn 0 gilt nur pv und extpv aus e3dc
    pvtotal = pv + extpv
    if (pvother == 0) or (pvtotal != 0):
        if pvother == 1:
            pvtotal = pvtotal + pvwattin
        log.debug(" wr update pvother %d pvtotal %d", pvother,pvtotal)
        cntpv= SimCountFactory().get_sim_counter()().sim_count(pvtotal, prefix="pv")
        get_inverter_value_store(1).set(InverterState(counter=cntpv[1], power=pvtotal))

def main(address1: str,address2: str, external: int,pvmodul: str,pvwattin: int):
    # external is 0 or 1
    log.debug("Beginning update")
    address = ['none']*2
    address[0]=address1
    address[1]=address2
    if pvmodul == "none":
        pvother = 0
    else:
        pvother = 1
    update_e3dc_battery(address,external,pvother,pvwattin)
    log.debug("Update completed successfully")

if __name__ == '__main__':
    setup_logging_stdout()
    run_using_positional_cli_args(main)
