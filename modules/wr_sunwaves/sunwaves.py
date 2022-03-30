#!/usr/bin/env python3
import logging
import re
import requests
from requests.auth import HTTPDigestAuth
from typing import List

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Sunwaves WR")


def update(wrsunwavesip: str, wrsunwavespw: str):
    log.debug('PV Sunwaves IP:' + wrsunwavesip)
    log.debug('PV Sunwaves Passwort:' + wrsunwavespw)

    params = (('CAN', '1'),)
    variable = requests.get("http://"+wrsunwavesip+"/data/ajax.txt",
                            params=params,
                            auth=HTTPDigestAuth("customer", wrsunwavespw),
                            timeout=3)
    variable.encoding = 'utf-8'
    variable = variable.text.replace("\n", "")

    count = 0

    for v in variable:
        if count == 1:
            pvwatt = re.search('^[0-9]+$', v).group()
            pvwatt = pvwatt*-1
            log.debug('WR Leistung: ' + str(pvwatt))
            with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
                f.write(str(pvwatt))
        if count == 16:
            log.debug('WR Energie: ' + str(v*1000))
            with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
                f.write(str(v*1000))
        count = count+1


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
