#!/usr/bin/python
import logging
from statistics import mean
from typing import Iterable, List

from pymodbus.constants import Endian

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import BatState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_bat_value_store

log = logging.getLogger("SolarEdge Battery")


def update_solaredge_battery(client: ModbusClient, slave_ids: Iterable[int]):
    all_socs = [client.read_holding_registers(
        62852, ModbusDataType.FLOAT_32, wordorder=Endian.Little, unit=slave_id
    ) for slave_id in slave_ids]
    storage_powers = [
        client.read_holding_registers(
            62836, ModbusDataType.FLOAT_32, wordorder=Endian.Little, unit=slave_id
        ) for slave_id in slave_ids
    ]
    log.debug("Battery SoCs=%s, powers=%s", all_socs, storage_powers)
    get_bat_value_store(1).set(BatState(power=sum(storage_powers), soc=mean(all_socs)))


def update(address: str, second_battery: int):
    # `second_battery` is 0 or 1
    log.debug("Beginning update")
    with ModbusClient(address) as client:
        update_solaredge_battery(client, range(1, 2 + second_battery))
    log.debug("Update completed successfully")


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
