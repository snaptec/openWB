#!/usr/bin/python
from pymodbus.constants import Endian
import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import CounterState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_counter_value_store
from modules.common.simcount import SimCountFactory

log = logging.getLogger("E3DC EVU")


def update(ipaddress: str):
    log.debug("Beginning update")
    with ModbusClient(ipaddress, port=502) as client:
        # 40074 EVU Punkt negativ -> Einspeisung in Watt
        power_all = client.read_holding_registers(40073, ModbusDataType.INT_32, wordorder=Endian.Little, unit=1)
        # 40130 Phasenleistung in Watt
        # max 6 Leistungsmesser verbaut ab 410105, typ 1 ist evu
        # bei den meisten e3dc auf 40128
        # for i in range (40104,40132,4):
        for i in range(40128, 40103, -4):
            # powers = client.read_holding_registers(40129, [ModbusDataType.INT_16] * 3, unit=1)
            powers = client.read_holding_registers(i, [ModbusDataType.INT_16] * 4, unit=1)
            log.debug("I: %d, p[0] typ %d p[1] a1 %d p[2] a2 %d p[3] a3 %d",
                      i, powers[0], powers[1], powers[2], powers[3])
            if powers[0] == 1:
                log.debug("Evu Leistungsmessung gefunden")
                break
    counter_import, counter_export = SimCountFactory().get_sim_counter()().sim_count(power_all, prefix="bezug")
    get_counter_value_store(1).set(CounterState(
        imported=counter_import,
        exported=counter_export,
        power=power_all,
        powers=powers[1:]
    ))
    log.debug("Update completed successfully")


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
