#!/usr/bin/env python3

import logging
from typing import List
from urllib.error import HTTPError

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import CounterState
from modules.common.powerwall import powerwall_update, PowerwallHttpClient
from modules.common.store import get_counter_value_store

log = logging.getLogger("Powerwall")


def update_using_powerwall_client(client: PowerwallHttpClient):
    # read firmware version
    status = client.get_json("/api/status")
    log.debug('Firmware: ' + status["version"])
    # read aggregate
    aggregate = client.get_json("/api/meters/aggregates")
    try:
        # read additional info if firmware supports
        meters_site = client.get_json("/api/meters/site")
        powerwall_state = CounterState(
            imported=aggregate["site"]["energy_imported"],
            exported=aggregate["site"]["energy_exported"],
            power=aggregate["site"]["instant_power"],
            voltages=[
                meters_site["0"]["Cached_readings"]["v_l" + str(phase) + "n"] for phase in range(1, 4)
            ],
            currents=[
                meters_site["0"]["Cached_readings"]["i_" + phase + "_current"] for phase in ["a", "b", "c"]
            ],
            powers=[
                meters_site["0"]["Cached_readings"]["real_power_" + phase] for phase in ["a", "b", "c"]
            ]
        )
    except [KeyError, HTTPError]:
        log.debug("Firmware seems not to provide detailed phase measurements. Fallback to total power only.")
        powerwall_state = CounterState(
            imported=aggregate["site"]["energy_imported"],
            exported=aggregate["site"]["energy_exported"],
            power=aggregate["site"]["instant_power"]
        )
    get_counter_value_store(1).set(powerwall_state)


def update(address: str, email: str, password: str):
    powerwall_update(address, email, password, update_using_powerwall_client)


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
