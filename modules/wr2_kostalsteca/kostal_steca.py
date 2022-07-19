#!/usr/bin/env python3
import logging
import xml.etree.ElementTree as ET
import re
import requests
from typing import List
from math import isnan

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("KostalSteca WR")


def update(pv2ip: str, variant: int):
    #
    # RainerW 8th of April 2020
    # Unfortunately Kostal has introduced the third version of interface: XML
    # This script is for Kostal_Piko_MP_plus and StecaGrid coolcept (single phase inverter)
    # In fact Kostal is not developing own single phase inverter anymore but is sourcing them from Steca
    # If you have the chance to test this module for the latest three phase inverter from Kostal (Plenticore)
    # or Steca (coolcept3 or coolcept XL) let us know if it works
    # DetMoerk 20210323: Anpassung für ein- und dreiphasige WR der Serie. Anstatt eine feste Zeile aus
    # dem Ergebnis zu schneiden wird nach der Zeile mit AC_Power gesucht.

    log.debug("PV Kostal Steca IP: " + pv2ip)
    log.debug("PV Kostal Steca Variant: " + str(variant))

    # call for XML file and parse it for current PV power
    measurements = requests.get("http://" + pv2ip + "/measurements.xml", timeout=2).text
    log.debug("measurements: " + str(measurements))
    power_kostal_piko_MP = float(ET.fromstring(measurements).find(".//Measurement[@Type='AC_Power']").get("Value")) * -1
    power_kostal_piko_MP = 0 if isnan(power_kostal_piko_MP) else int(power_kostal_piko_MP)
    # allow only numbers
    regex = '^-?[0-9]+$'
    if re.search(regex, str(power_kostal_piko_MP)) is None:
        power_kostal_piko_MP = "0"
    log.debug("PVWatt: " + str(power_kostal_piko_MP))

    # call for XML file and parse it for total produced kwh
    yields_xml = "yields.xml"
    yields = requests.get("http://" + pv2ip + "/" + yields_xml, timeout=2).text
    log.debug("YIELD: " + yields)

    if variant == 0:
        pvkwh_kostal_piko_MP = int(float(ET.fromstring(yields).find(
            ".//Yield[@Type='Produced']/YieldValue").get("Value")))
    else:
        yields_js = "gen.yield.total.chart.js"
        # call for .js file and parse it for total produced Wh
        yields = requests.get("http://" + pv2ip + "/" + yields_js, timeout=2).text
        log.debug("YIELD: " + yields)
        match = re.search(r'"data":\s*\[\s*([^\]]*)\s*]', yields)
        try:
            pvkwh_kostal_piko_MP = int(sum(float(s) * 1e6 for s in match.group(1).split(',')))
        except AttributeError:
            log.debug("PVkWh: Could not find 'data' in " + yields_js + ".")

    if "pvkwh_kostal_piko_MP" not in locals() or re.search(regex, str(pvkwh_kostal_piko_MP)) is None:
        log.debug("PVkWh: NaN get prev. Value")
        with open("/var/www/html/openWB/ramdisk/pv2kwh", "r") as f:
            pvkwh_kostal_piko_MP = f.read()
    log.debug('PVkWh: '+str(pvkwh_kostal_piko_MP))

    # Daten in Ramdisk schreiben
    log.debug("WR Energie: " + str(pvkwh_kostal_piko_MP))
    with open("/var/www/html/openWB/ramdisk/pv2kwh", "w") as f:
        f.write(str(pvkwh_kostal_piko_MP))
    log.debug("WR Leistung: " + str(power_kostal_piko_MP))
    with open("/var/www/html/openWB/ramdisk/pv2watt", "w") as f:
        f.write(str(power_kostal_piko_MP))


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
