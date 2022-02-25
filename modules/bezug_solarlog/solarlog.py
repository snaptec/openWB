#!/usr/bin/env python3
from typing import List
import json
import logging
import requests
import traceback

from helpermodules.cli import run_using_positional_cli_args


log = logging.getLogger("Solarlog EVU")


def update(bezug_solarlog_ip: str, bezug_solarlog_speicherv: str):
    log.debug('Solarlog IP: ' + bezug_solarlog_ip)
    log.debug('Solarlog Speicher: ' + bezug_solarlog_speicherv)

    data = {"801": {"170": None}}
    data = json.dumps(data)
    response = requests.post('http://'+bezug_solarlog_ip+'/getjp', data=data, timeout=3).json()

    try:
        pvwatt = response["801"]["170"]["101"]
    except:
        traceback.print_exc()
        exit(1)
    try:
        hausverbrauch = response["801"]["170"]["110"]
    except:
        traceback.print_exc()
        exit(1)
    bezugwatt = hausverbrauch - pvwatt
    try:
        pvkwh = response["801"]["170"]["109"]
    except:
        traceback.print_exc()
        exit(1)

    if bezug_solarlog_speicherv == 1:
        with open("ramdisk/speicherleistung", "r") as f:
            speicherleistung = f.read()
        bezugwatt = bezugwatt + speicherleistung
    if pvwatt > 5:
        pvwatt = pvwatt*-1

    log.debug('Leistung: ' + str(bezugwatt))
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(bezugwatt))
    log.debug('PV Leistung: ' + str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(pvwatt))
    with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
        f.write(str(pvkwh))
    pvkwhk = pvkwh*1000
    with open("/var/www/html/openWB/ramdisk/pvkwhk", "w") as f:
        f.write(str(pvkwhk))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
