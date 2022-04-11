#!/usr/bin/python
import logging
import math
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import CounterState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_counter_value_store

log = logging.getLogger("SolarEdge EVU")


def scale_registers(registers: List[int]) -> List[float]:
    scale = math.pow(10, registers[-1])
    return [register * scale for register in registers[:-1]]


def update(ipaddress: str, modbusport: int, slaveid: int):
    log.debug("Beginning update")

    def read_scaled_int16(address: int, count: int):
        return scale_registers(
            client.read_holding_registers(address, [ModbusDataType.INT_16] * (count+1), unit=slaveid)
        )

    with ModbusClient(ipaddress, port=modbusport) as client:
        # 40206: Total Real Power (sum of active phases)
        # 40206/40207/40208: Real Power by phase
        # 40210: AC Real Power Scale Factor
        powers = [-power for power in read_scaled_int16(40206, 4)]

        # 40191/40192/40193: AC Current by phase
        # 40194: AC Current Scale Factor
        currents = read_scaled_int16(40191, 3)

        # 40196/40197/40198: Voltage per phase
        # 40203: AC Voltage Scale Factor
        voltages = read_scaled_int16(40196, 7)[:3]

        # 40204: AC Frequency
        # 40205: AC Frequency Scale Factor
        frequency, = read_scaled_int16(40204, 1)

        # 40222/40223/40224: Power factor by phase (unit=%)
        # 40225: AC Power Factor Scale Factor
        power_factors = [power_factor / 100 for power_factor in read_scaled_int16(40222, 3)]

        # 40234: Total Imported Real Energy
        counter_imported = client.read_holding_registers(40234, ModbusDataType.UINT_32, unit=slaveid)

        # 40226: Total Exported Real Energy
        counter_exported = client.read_holding_registers(40226, ModbusDataType.UINT_32, unit=slaveid)

    get_counter_value_store(1).set(CounterState(
        imported=counter_imported,
        exported=counter_exported,
        power=powers[0],
        powers=powers[1:],
        voltages=voltages,
        currents=currents,
        power_factors=power_factors,
        frequency=frequency
    ))
    log.debug("Update completed successfully")


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
