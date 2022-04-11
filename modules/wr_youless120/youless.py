#!/usr/bin/env python3
import logging
import requests
import traceback
from typing import List

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Youless WR")


def update(wryoulessip: str, wryoulessalt: int):
    log.debug('PV Youless IP:' + wryoulessip)
    log.debug('PV Youless Alternative:' + str(wryoulessalt))

    # Auslesen vom S0-Eingang eines Youless LS120 Energy Monitor.
    params = (('f', 'j'),)
    answer = requests.get("http://"+wryoulessip+'/a', params=params, timeout=5).json()
    if wryoulessalt == 0:
        try:
            # aktuelle Ausgangsleistung am WR [W]
            pvwatt = int(answer["ps0"])
            # Gesamtz‰hlerstand am WR [Wh]
            pvkwh = answer["cs0"]
            pvkwh = pvkwh.replace(",", "")
        except:
            traceback.print_exc()
            exit(1)
    else:
        try:
            # aktuelle Ausgangsleistung am WR [W]
            pvwatt = int(answer["pwr"])
            # Gesamtz‰hlerstand am WR [Wh]
            pvkwh = answer["cnt"]
            pvkwh = pvkwh.replace(",", "")
        except:
            traceback.print_exc()
            exit(1)

    if pvwatt > 5:
        pvwatt = pvwatt*-1
    log.debug('WR Leistung: ' + str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    log.debug('WR Energie: ' + str(pvkwh))
    with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
        f.write(str(pvkwh))
    # Gesamtzählerstand am WR [kWh]
    pvkwh = pvkwh/1000
    with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
        f.write(str(pvkwh))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
