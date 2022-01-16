#!/usr/bin/env python3
import logging

import requests

from helpermodules.cli import run_using_positional_cli_args
from helpermodules.log import setup_logging_stdout
from modules.common.component_state import CounterState
from modules.common.store import get_counter_value_store

setup_logging_stdout()
log = logging.getLogger("EVU Discovergy")


def get_last_reading(user: str, password: str, meter_id: str):
    response = requests.get(
        "https://api.discovergy.com/public/v1/last_reading",
        params={"meterId": meter_id},
        auth=(user, password),
        timeout=3
    )
    response.raise_for_status()
    return response.json()


def write_readings_to_ramdisk(discovergy: dict):
    values = discovergy["values"]
    try:
        voltages = [values["voltage" + str(phase)] / 1000 for phase in range(1, 4)]
    # Es gibt verschiedene Antworten vom Discovergy-Modul.
    except KeyError:
        try:
            voltages = [values["phase" + str(phase) + "Voltage"] / 1000 for phase in range(1, 4)]
        except KeyError:
            # Some discovergy counters do not report voltage at all
            voltages = None
    try:
        powers = [values["power" + str(phase)] / 1000 for phase in range(1, 4)]
    except KeyError:
        powers = [values["phase" + str(phase) + "Power"] / 1000 for phase in range(1, 4)]
    power_total = values["power"] / 1000

    get_counter_value_store(1).set(CounterState(
        imported=values["energy"] / 10000000,
        exported=values["energyOut"] / 10000000,
        power=power_total,
        voltages=voltages,
        currents=[power / voltage for power, voltage in zip(powers, [230] * 3 if voltages is None else voltages)],
        powers=powers
    ))
    log.debug("Update complete. Total Power: %g W", power_total)


def update(user: str, password: str, meter_id: str):
    log.debug("Beginning update")
    write_readings_to_ramdisk(get_last_reading(user, password, meter_id))
    log.debug("Update completed successfully")


if __name__ == '__main__':
    run_using_positional_cli_args(update)
