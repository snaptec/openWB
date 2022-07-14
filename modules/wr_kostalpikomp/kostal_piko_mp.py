#!/usr/bin/env python3
import logging
import xml.etree.ElementTree as ET
import re
import requests
from typing import List
from math import isnan

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("KostalPikoMP WR")

def update(pvip: str):
    #
    # andlem74 July 13, 2022
    # This module is based on wr2_kostalsteca.
    # For Kostal Piko MP (non-plus) inverters, unfortunately, the yield.xml is empty.
    # Therefore, the yield values are calculated from the .js that generates the graph
    # in the web interface.
 
    log.debug("PV KostalPikoMP IP: " + pvip)

    # call for XML file and parse it for current PV power
    measurements = requests.get("http://" + pvip + "/measurements.xml", timeout=2).text
    log.debug("measurements: " + str(measurements))
    power_kostal_piko_MP = float(ET.fromstring(measurements).find(".//Measurement[@Type='AC_Power']").get("Value")) * -1
    power_kostal_piko_MP = 0 if isnan(power_kostal_piko_MP) else int(power_kostal_piko_MP)
    # allow only numbers
    regex = '^-?[0-9]+$'
    if re.search(regex, str(power_kostal_piko_MP)) is None:
        power_kostal_piko_MP = 0
    log.debug("PVWatt: " + str(power_kostal_piko_MP))

    # call for .js file and parse it for total produced Wh
    yields = requests.get("http://" + pvip + "/gen.yield.total.chart.js", timeout=2).text
    log.debug("YIELD: " + yields)
    match = re.search(r'"data":\s*\[\s*([^\]]*)\s*]', yields);
    if (match):
        pvkwh_kostal_piko_MP = int(sum(float(s) * 1e6 for s in match.group(1).split(',')))
 
    if (match is None or re.search(regex, str(pvkwh_kostal_piko_MP)) is None):
        log.debug("PVkWh: NaN get prev. Value")
        with open("/var/www/html/openWB/ramdisk/pvkwh", "r") as f:
            pvkwh_kostal_piko_MP = f.read()
    log.debug('PVkWh: '+str(pvkwh_kostal_piko_MP))

    # Daten in Ramdisk schreiben
    log.debug("WR Energie: " + str(pvkwh_kostal_piko_MP))
    with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
        f.write(str(pvkwh_kostal_piko_MP))
    log.debug("WR Leistung: " + str(power_kostal_piko_MP))
    with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
        f.write(str(power_kostal_piko_MP))

def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)