#!/usr/bin/env python3
import logging
import math
from statistics import mean
from typing import List

from pymodbus.constants import Endian

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.component_state import InverterState, BatState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_inverter_value_store, get_bat_value_store

# Sunspec (API) documentation: https://www.solaredge.com/sites/default/files/sunspec-implementation-technical-note.pdf


log = logging.getLogger("SolarEdge")


def update_solar_edge(client: ModbusClient,
                      slave_ids: List[int],
                      batwrsame: int,
                      extprodakt: int,
                      zweiterspeicher: int,
                      subbat: int):
    storage_slave_ids = slave_ids[0: 1 + zweiterspeicher]
    storage_powers = []
    if batwrsame == 1:
        all_socs = [client.read_holding_registers(
            62852, ModbusDataType.FLOAT_32, wordorder=Endian.Little, unit=slave_id
        ) for slave_id in storage_slave_ids]
        storage_powers = [
            client.read_holding_registers(
                62836, ModbusDataType.FLOAT_32, wordorder=Endian.Little, unit=slave_id
            ) for slave_id in storage_slave_ids
        ]
        log.debug("Battery SoCs=%s, powers=%s", all_socs, storage_powers)
        get_bat_value_store(1).set(BatState(power=sum(storage_powers), soc=mean(all_socs)))

    total_energy = 0
    total_power = 0
    total_currents = [0, 0, 0]

    for slave_id in slave_ids:
        # 40083 = AC Power value (Watt), 40084 = AC Power scale factor
        power_base, power_scale = client.read_holding_registers(40083, [ModbusDataType.INT_16] * 2, unit=slave_id)
        total_power -= power_base * math.pow(10, power_scale)
        # 40093 = AC Lifetime Energy production (Watt hours)
        energy = client.read_holding_registers(40093, ModbusDataType.INT_32, unit=slave_id)
        total_energy += energy
        # 40072/40073/40074 = AC Phase A/B/C Current value (Amps)
        # 40075 = AC Current scale factor
        currents = client.read_holding_registers(
            40072, [ModbusDataType.UINT_16] * 3 + [ModbusDataType.INT_16], unit=slave_id
        )
        log.debug(
            "slave=%d: power=%d*10^%d, energy=%d, currents=%s * 10^%d",
            slave_id, power_base, power_scale, energy, currents[0:3], currents[3]
        )
        currents_scale = math.pow(10, currents[3])
        for i in range(3):
            total_currents[i] += currents[i] * currents_scale
    if extprodakt == 1:
        # 40380 = "Meter 2/Total Real Power (sum of active phases)" (Watt)
        total_power -= client.read_holding_registers(40380, ModbusDataType.INT_16, unit=slave_ids[0])
    if subbat == 1:
        total_power -= sum(min(p, 0) for p in storage_powers)
    else:
        total_power -= sum(storage_powers)

    get_inverter_value_store(1).set(InverterState(
        counter=total_energy, power=total_power, currents=total_currents
    ))


def update_solar_edge_cli(ipaddress: str,
                          slave_id0: str,
                          slave_id1: str,
                          slave_id2: str,
                          slave_id3: str,
                          batwrsame: int,
                          extprodakt: int,
                          zweiterspeicher: int,
                          subbat: int):
    log.debug("Beginning update")
    with ModbusClient(ipaddress) as client:
        update_solar_edge(
            client,
            list(map(int, filter(lambda id: id.isnumeric(), [slave_id0, slave_id1, slave_id2, slave_id3]))),
            batwrsame,
            extprodakt,
            zweiterspeicher,
            subbat
        )
    log.debug("Update completed successfully")


if __name__ == '__main__':
    setup_logging_stdout()
    run_using_positional_cli_args(update_solar_edge_cli)
