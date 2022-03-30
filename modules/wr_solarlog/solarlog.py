#!/usr/bin/env python3
from typing import List
import json
import logging
import requests

from helpermodules.cli import run_using_positional_cli_args
from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store

log = logging.getLogger("Solarlog WR")


def update(bezug_solarlog_ip: str):
    log.debug('Wechselrichter Solarlog IP: ' + bezug_solarlog_ip)

    data = {"801": {"170": None}}
    data = json.dumps(data)
    response = requests.post("http://"+bezug_solarlog_ip+'/getjp', data=data, timeout=3).json()
    pv_watt = response["801"]["170"]["101"]
    pv_kwh = response["801"]["170"]["109"]

    if pv_watt > 5:
        pv_watt = pv_watt*-1


    log.debug('WR Leistung: ' + str(pv_watt))
    log.debug('WR Energie: ' + str(pv_kwh))

    get_inverter_value_store(1).set(InverterState(counter=pv_kwh, power=pv_watt))

def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)