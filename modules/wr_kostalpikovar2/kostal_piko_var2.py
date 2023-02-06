#!/usr/bin/env python3
import logging
import re
from typing import List

import requests

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store

log = logging.getLogger("Kostal Piko Var2")


def parse_kostal_piko_var2_html(html: str):
    # power may be a string "xxx" when the inverter is offline, so we cannot match as a number
    # state is just for debugging currently known states:
    # - Aus
    # - Leerlauf
    result = re.search(
        r"aktuell</td>\s*<td[^>]*>\s*([^<]+).*"
        r"Gesamtenergie</td>\s*<td[^>]*>\s*(\d+).*"
        r"Status</td>\s*<td[^>]*>\s*([^<]+)",
        html,
        re.DOTALL
    )
    if result is None:
        raise Exception("Given HTML does not match the expected regular expression. Ignoring.")
    log.debug("Inverter data: state=%s, power=%s, exported=%s" % (result.group(3), result.group(1), result.group(2)))
    try:
        power = -int(result.group(1))
    except ValueError:
        log.info("Inverter power is not a number! Inverter may be offline. Setting power to 0 W.")
        power = 0
    return InverterState(
        exported=int(result.group(2)) * 1000,
        power=power
    )


def update(num: int, wr_piko2_url: str, wr_piko2_user: str, wr_piko2_pass: str):
    log.debug("Beginning update")
    response = requests.get(wr_piko2_url, verify=False, auth=(wr_piko2_user, wr_piko2_pass), timeout=10)
    response.raise_for_status()
    get_inverter_value_store(num).set(parse_kostal_piko_var2_html(response.text))
    log.debug("Update completed successfully")


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
