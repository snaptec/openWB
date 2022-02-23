#!/usr/bin/env python3

import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import InverterState
from modules.common.powerwall import PowerwallHttpClient, powerwall_update
from modules.common.store import get_inverter_value_store, RAMDISK_PATH

COOKIE_FILE = RAMDISK_PATH / "powerwall_cookie.txt"
log = logging.getLogger("Powerwall")


def update_using_powerwall_client(client: PowerwallHttpClient):
    aggregate = client.get_json("/api/meters/aggregates")
    pv_watt = aggregate["solar"]["instant_power"]
    if pv_watt > 5:
        pv_watt = pv_watt*-1
    get_inverter_value_store(1).set(InverterState(
        counter=aggregate["solar"]["energy_exported"],
        power=pv_watt
    ))


def update(address: str, email: str, password: str):
    powerwall_update(address, email, password, update_using_powerwall_client)


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
