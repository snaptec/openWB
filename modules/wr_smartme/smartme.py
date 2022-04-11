#!/usr/bin/env python3
import logging
import requests
from typing import List

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store

log = logging.getLogger("SmartMe WR")


def update(wr_smartme_url: str, wr_smartme_user: str, wr_smartme_pass: str):
    log.debug('Wechselrichter smartme URL: ' + wr_smartme_url)
    log.debug('Wechselrichter smartme User: ' + wr_smartme_user)
    log.debug('Wechselrichter smartme Passwort: ' + wr_smartme_pass)

    # Daten einlesen
    response = requests.get(wr_smartme_url, auth=(wr_smartme_user, wr_smartme_pass), timeout=3).json()
    # Aktuelle Leistung (kW --> W)
    wattwr = response["ActivePower"]
    wattwr = round(wattwr * 1000)

    # Zählerstand Export (kWh --> Wh)
    pvkwh = response["CounterReadingExport"]
    pvkwh = round(pvkwh * 1000, 3)

    log.debug('WR Leistung: ' + str(wattwr))
    log.debug('WR Energie: ' + str(pvkwh))

    get_inverter_value_store(1).set(InverterState(counter=pvkwh, power=wattwr))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
