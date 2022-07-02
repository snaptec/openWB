#!/usr/bin/env python3
from typing import List
import logging
import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Solarworld EVU")


def update(solarworld_emanagerip: str):
    log.debug('Solarworld IP: ' + solarworld_emanagerip)

    # Auslesen eines Solarworld eManagers über die integrierte JSON-API
    emanagerantwort = requests.get(
        'http://'+solarworld_emanagerip+'/rest/solarworld/lpvm/powerAndBatteryData', timeout=3).json()
    try:
        em_in_watt = emanagerantwort["PowerIn"]
    except:
        traceback.print_exc()
        exit(1)
    try:
        em_out_watt = emanagerantwort["PowerOut"]
    except:
        traceback.print_exc()
        exit(1)

    # Bezug ist entweder -Out oder In; bei Einspeisung ist 'em_in_watt' immer 0
    bezug_watt = int(em_in_watt - em_out_watt)

    log.debug('Leistung: ' + str(bezug_watt))
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(bezug_watt))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
