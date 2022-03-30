#!/usr/bin/env python3

import logging
from typing import List

import requests

from modules.common.component_state import InverterState
from modules.common.store import get_inverter_value_store
from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Kostal-Piko")


def update(num: int, speichermodul: str, wrkostalpikoip: str):
    log.debug('Wechselrichter Kostal Piko Var 1 Speicher: ' + speichermodul)
    log.debug('Wechselrichter Kostal Piko Var 1 IP: ' + wrkostalpikoip)

    # Auslesen eines Kostal Piko WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung.
    if speichermodul != "none":
        params = (('dxsEntries', ['33556736', '251658753)']),)
        pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=5).json()
    else:
        params = (('dxsEntries', ['67109120', '251658753)']),)
        pvwatttmp = requests.get('http://'+wrkostalpikoip+'/api/dxs.json', params=params, timeout=5).json()

    # aktuelle Ausgangsleistung am WR [W]
    pvwatt = int(pvwatttmp["dxsEntries"][0]["value"])

    if pvwatt > 5:
        pvwatt = pvwatt*-1

    log.debug('WR Leistung: ' + str(pvwatt))
    # Gesamtzählerstand am WR [kWh]
    pvkwh = int(pvwatttmp['dxsEntries'][1]['value'])

    get_inverter_value_store(num).set(InverterState(counter=pvkwh*1000, power=pvwatt))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
