#!/usr/bin/env python3

import logging
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import BatState
from modules.common.powerwall import powerwall_update, PowerwallHttpClient
from modules.common.store import get_bat_value_store, RAMDISK_PATH

COOKIE_FILE = RAMDISK_PATH / "powerwall_cookie.txt"
log = logging.getLogger("Powerwall")


def update_using_powerwall_client(client: PowerwallHttpClient):
    aggregate = client.get_json("/api/meters/aggregates")
    get_bat_value_store(1).set(BatState(
        imported=aggregate["battery"]["energy_imported"],
        exported=aggregate["battery"]["energy_exported"],
        power=-aggregate["battery"]["instant_power"],
        soc=client.get_json("/api/system_status/soe")["percentage"]
    ))


def update(address: str, email: str, password: str):
    powerwall_update(address, email, password, update_using_powerwall_client)


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
