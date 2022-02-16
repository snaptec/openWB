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
    result = re.search(r"aktuell</td>\s*<td[^>]*>\s*(\d+).*Gesamtenergie</td>\s*<td[^>]*>\s*(\d+)", html, re.DOTALL)
    if result is None:
        raise Exception("Given HTML does not match the expected regular expression. Ignoring.")
    return InverterState(
        counter=int(result.group(2)) * 1000,
        power=-int(result.group(1))
    )


def update(num: int, wr_piko2_url: str, wr_piko2_user: str, wr_piko2_pass: str):
    log.debug("Beginning update")
    response = requests.get(wr_piko2_url, verify=False, auth=(wr_piko2_user, wr_piko2_pass), timeout=10)
    response.raise_for_status()
    get_inverter_value_store(num).set(parse_kostal_piko_var2_html(response.text))
    log.debug("Update completed successfully")


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
