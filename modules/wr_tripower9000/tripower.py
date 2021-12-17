#!/usr/bin/env python3
import logging
import sys
from typing import Iterable

import requests

from helpermodules.log import setup_logging_stdout
from modules.common.component_state import InverterState
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_inverter_value_store

SMA_INT32_NAN = -0x80000000  # SMA uses this value to represent NaN
log = logging.getLogger("SMA ModbusTCP WR")


def update_sma_webbox(address: str):
    data = {'RPC': '{"version": "1.0","proc": "GetPlantOverview","id": "1","format": "JSON"}'}
    response = requests.post('http://' + address + '/rpc', json=data, timeout=3)
    response.raise_for_status()
    response_data = response.json()
    get_inverter_value_store(1).set(InverterState(
        counter=response_data["result"]["overview"][2]["value"] * 1000,
        power=-response_data["result"]["overview"][0]["value"]
    ))


def update_sma_modbus(addresses: Iterable[str]):
    power_total = 0
    energy_total = 0

    for ipaddress in addresses:
        with ModbusClient(ipaddress) as client:
            # AC Wirkleistung über alle Phasen (W) [Pac]:
            power = client.read_holding_registers(30775, ModbusDataType.INT_32, unit=3)
            # Gesamtertrag (Wh) [E-Total]:
            energy = client.read_holding_registers(30529, ModbusDataType.UINT_32, unit=3)

            log.debug("%s: power = %d W, energy = %d Wh", ipaddress, power, energy)
            if power == SMA_INT32_NAN:
                log.debug("Power value is NaN - ignoring")
            else:
                power_total += power
            energy_total += energy

    power_total = -max(power_total, 0)
    get_inverter_value_store(1).set(InverterState(counter=energy_total, power=power_total))


def update_sma():
    log.debug("Beginning update")
    if sys.argv[1] == "1":
        update_sma_webbox(sys.argv[2])
    else:
        update_sma_modbus(filter("none".__ne__, sys.argv[2:]))
    log.debug("Update completed successfully")


if __name__ == '__main__':
    setup_logging_stdout()
    update_sma()
