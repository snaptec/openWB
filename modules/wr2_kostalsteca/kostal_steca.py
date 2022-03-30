#!/usr/bin/env python3
import logging
import xml.etree.ElementTree as ET
import re
import requests
from typing import List

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("KostalSteca WR")


def update(pv2ip: str):
    #
    # RainerW 8th of April 2020
    # Unfortunately Kostal has introduced the third version of interface: XML
    # This script is for Kostal_Piko_MP_plus and StecaGrid coolcept (single phase inverter)
    # In fact Kostal is not developing own single phase inverter anymore but is sourcing them from Steca
    # If you have the chance to test this module for the latest three phase inverter from Kostal (Plenticore) or Steca (coolcept3 or coolcept XL) let us know if it works
    # DetMoerk 20210323: Anpassung fuer ein- und dreiphasige WR der Serie. Anstatt eine feste Zeile aus dem Ergebnis zu schneiden wird nach der Zeile mit AC_Power gesucht.

    log.debug('PV Kostal Steca IP:' + pv2ip)

    # call for XML file and parse it for current PV power
    response = requests.get("http://"+pv2ip+"/measurements.xml", timeout=2).text
    log.debug("MEASURE: "+str(response))
    power_kostal_piko_MP = ET.fromstring(response).find("Measurement[@Type='AC_Power']").get("Value")

    # cut the comma and the digit behind the comma
    power_kostal_piko_MP = int(float(power_kostal_piko_MP))

    # allow only numbers
    regex = '^-?[0-9]+$'
    if re.search(regex, str(power_kostal_piko_MP)) == None:
        power_kostal_piko_MP = "0"

    log.debug("'PVWatt: "+str(power_kostal_piko_MP)+"'")

    # call for XML file and parse it for total produced kwh
    yields = requests.get("http://"+pv2ip+"/yields.xml", timeout=2).text
    log.debug("YIELD: "+yields)

    response = requests.get("http://"+pv2ip+"/yields.xml", timeout=2).text
    pvkwh_kostal_piko_MP = ET.fromstring(response).find("YieldValue").get("Value")

    if re.search(regex, str(pvkwh_kostal_piko_MP)) == None:
        log.debug("PVkWh: NaN get prev. Value")
        with open("/var/www/html/openWB/ramdisk/pv2kwh", "r") as f:
            pvkwh_kostal_piko_MP = f.read()

    log.debug('PVkWh: '+str(pvkwh_kostal_piko_MP))

    # Daten in Ramdisk schreiben
    log.debug('WR Energie: ' + str(pvkwh_kostal_piko_MP))
    with open("/var/www/html/openWB/ramdisk/pv2kwh", "w") as f:
        f.write(str(pvkwh_kostal_piko_MP))
    log.debug('WR Leistung: ' + "-"+str(power_kostal_piko_MP))
    with open("/var/www/html/openWB/ramdisk/pv2watt", "w") as f:
        f.write("-"+str(power_kostal_piko_MP))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
