#!/usr/bin/env python3
import logging
from typing import List

import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("PowerFox")


def update(powerfoxid: str, powerfoxuser: str, powerfoxpass: str):
    log.debug('Powerfox ID: ' + powerfoxid)
    log.debug('Powerfox User: ' + powerfoxuser)
    log.debug('Powerfox Passwort: ' + powerfoxpass)

    response = requests.get('https://backend.powerfox.energy/api/2.0/my/'+powerfoxid +
                            '/current', auth=(powerfoxuser, powerfoxpass), timeout=3).json()
    try:
        einspeisungwh = int(response['A_Minus'])
        with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
            f.write(str(einspeisungwh))
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Einspeisung: ' + str(einspeisungwh))

    try:
        bezugwh = int(response['A_Plus'])
        with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
            f.write(str(bezugwh))
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Bezug: ' + str(bezugwh))

    try:
        watt = int(response['Watt'])
        with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
            f.write(str(watt))
    except:
        traceback.print_exc()
        exit(1)
    log.debug('Watt: ' + str(watt))

def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
