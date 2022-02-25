#!/usr/bin/env python3
import logging
import re
import requests
import traceback
from typing import Dict, List

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("SmartMe EVU")


def get_power_value(key, response: Dict, file=None):
    try:
        value = int(response[key] * 1000)
        if file == None:
            return value
        else:
            log.debug(file+': ' + str(value))
            f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
            f.write(str(value))
            f.close()
    except:
        traceback.print_exc()
        exit(1)


def get_im_ex_value(key, response: Dict, file):
    try:
        value = round(response[key] * 1000, 3)
        log.debug(file+': ' + str(value))
        f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
        f.write(str(value))
        f.close()
    except:
        traceback.print_exc()
        exit(1)


def get_value(key, response: Dict, file=None):
    try:
        value = response[key]
        if file == None:
            return value
        else:
            log.debug(file+': ' + str(value))
            f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
            f.write(str(value))
            f.close()
    except:
        traceback.print_exc()
        exit(1)


def update(bezug_smartme_url: str, bezug_smartme_user: str, bezug_smartme_pass: str):
    log.debug('Smartme URL: ' + bezug_smartme_url)
    log.debug('Smartme User: ' + bezug_smartme_user)
    log.debug('Smartme Passwort: ' + bezug_smartme_pass)

    # Daten einlesen
    response = requests.get(bezug_smartme_url, auth=(bezug_smartme_user, bezug_smartme_pass), timeout=3).json()

    # Aktuelle Leistung (kW --> W)
    wattbezug = get_power_value("ActivePower", response)
    wattbezug1 = get_power_value("ActivePowerL1", response)
    if wattbezug1 == 0:
        wattbezug1 = wattbezug
    get_power_value("ActivePowerL2", response, "bezugw2")
    get_power_value("ActivePowerL3", response, "bezugw3")
    # Zählerstand Import(kWh)
    get_im_ex_value("CounterReadingImport", response, "bezugkwh")
    # Zählerstand Export(kWh)
    get_im_ex_value("CounterReadingExport", response, "einspeisungkwh")

    # Weitere Zählerdaten für die Statusseite (PowerFaktor, Spannung und Strom)
    get_value("PowerFactorL1", response, "evupf1")
    get_value("PowerFactorL2", response, "evupf2")
    get_value("PowerFactorL3", response, "evupf3")
    get_value("VoltageL1", response, "evuv1")
    get_value("VoltageL2", response, "evuv2")
    get_value("VoltageL3", response, "evuv3")
    bezuga1 = get_value("CurrentL1", response)
    if bezuga1 is None:
        try:
            bezuga1 = response["Current"]
        except:
            traceback.print_exc()
            exit(1)
    log.debug('Strom L1: ' + str(bezuga1))
    with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
        f.write(str(bezuga1))
    get_value("CurrentL2", response, "bezuga2")
    get_value("CurrentL3", response, "bezuga3")

    # Prüfen ob Werte gültig
    regex = '^[-+]?[0-9]+.?[0-9]*$'
    if re.search(regex, str(wattbezug)) == None:
        with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
            wattbezug = f.read()
    # Ausgabe
    log.debug('Leistung: ' + str(wattbezug))
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(wattbezug))
    log.debug('Leistung L1: ' + str(wattbezug1))
    with open("/var/www/html/openWB/ramdisk/wattbezugw1", "w") as f:
        f.write(str(wattbezug1))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
