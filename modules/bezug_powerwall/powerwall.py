#!/usr/bin/env python3

import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import CounterState
from modules.common.powerwall import powerwall_update, PowerwallHttpClient
from modules.common.store import get_counter_value_store

log = logging.getLogger("Powerwall")


def update_using_powerwall_client(client: PowerwallHttpClient):
    # read firmware version
    status = client.get_json("/api/status")
    # since 21.44.1 tesla adds the commit hash '21.44.1 c58c2df3'
    # so we split by whitespace and take the first element for comparison
    log.debug('Firmware: ' + status["version"])
    firmwareversion = int(''.join(status["version"].split()[0].split(".")))
    # read aggregate
    aggregate = client.get_json("/api/meters/aggregates")
    # read additional info if firmware supports
    if firmwareversion >= 20490:
        meters_site = client.get_json("/api/meters/site")
        get_counter_value_store(1).set(CounterState(
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
        ))
    else:
        get_counter_value_store(1).set(CounterState(
            imported=aggregate["site"]["energy_imported"],
            exported=aggregate["site"]["energy_exported"],
            power=aggregate["site"]["instant_power"]
        ))


def update(address: str, email: str, password: str):
    powerwall_update(address, email, password, update_using_powerwall_client)


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
