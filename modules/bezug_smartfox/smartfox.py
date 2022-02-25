#!/usr/bin/env python3
import logging
import re
import requests
import traceback
import xml.etree.ElementTree as ET
from typing import List

from helpermodules.cli import run_using_positional_cli_args

log = logging.getLogger("Smartfox EVU")

def get_xml_text(root, tag, attribute_key, attribute_value):
    try:
        value = None
        for element in root.iter(tag):
            if element.get(attribute_key) == attribute_value:
                value = element.text
        return value
    except:
        traceback.print_exc()
        exit(1)

def update(bezug_smartfox_ip: str):
    log.debug('Smartfox IP: ' + bezug_smartfox_ip)

    # Anpassung der Variablennamen nach Firmwareupgrade auf EM2 00.01.03.06 (04-2021)
    # Daten einlesen
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Host': bezug_smartfox_ip,
        'Connection': 'keep-alive)',
    }

    response = requests.get('http://'+bezug_smartfox_ip+'/values.xml', headers=headers, timeout=5)
    response.encoding = 'utf-8'
    response = response.text.replace("\n", "")
    # Version ermitteln
    version = None
    root = ET.fromstring(response)
    version = get_xml_text(root, "value", "id", "version")
    if len(version) < 6:
        versionshort = version[:-6]
    else:
        versionshort = "oldversion"


    if versionshort != "EM2 00.01":
        newversion = True
        var_wattbezug = "detailsPowerValue"
        var_wattbezug1 = "powerL1Value"
        var_wattbezug2 = "powerL2Value"
        var_wattbezug3 = "powerL3Value"
        var_ikwh = "energyValue"
        var_ekwh = "eToGridValue"
        var_evupf1 = "not_available"
        var_evupf2 = "not_available"
        var_evupf3 = "not_available"
        var_evuv1 = "voltageL1Value"
        var_evuv2 = "voltageL2Value"
        var_evuv3 = "voltageL3Value"
        var_bezuga1 = "ampereL1Value"
        var_bezuga2 = "ampereL2Value"
        var_bezuga3 = "ampereL3Value"
    else:
        newversion = False
        var_wattbezug = "u5790-41"
        var_wattbezug1 = "u6017-41"
        var_wattbezug2 = "u6014-41"
        var_wattbezug3 = "u6011-41"
        var_ikwh = "u5827-41"
        var_ekwh = "u5824-41"
        var_evupf1 = "u6074-41"
        var_evupf2 = "u6083-41"
        var_evupf3 = "u6086-41"
        var_evuv1 = "u5978-41"
        var_evuv2 = "u5981-41"
        var_evuv3 = "u5984-41"
        var_bezuga1 = "u5999-41"
        var_bezuga2 = "u5996-41"
        var_bezuga3 = "u5993-41"


    # Aktuelle Leistung (kW --> W)
    wattbezug = (get_xml_text(root, "value", "id", var_wattbezug))[:-2]
    wattbezug1 = get_xml_text(root, "value", "id", var_wattbezug1)
    wattbezug2 = get_xml_text(root, "value", "id", var_wattbezug2)
    wattbezug3 = get_xml_text(root, "value", "id", var_wattbezug3)

    # Zählerstand Import(kWh)
    ikwh = (get_xml_text(root, "value", "id", var_ikwh))[:-4]
    ikwh = round(float(ikwh) * 1000, 2)
    ikwh = str(ikwh)

    # Zählerstand Export(kWh)
    ekwh = (get_xml_text(root, "value", "id", var_ekwh))[:-4]
    ekwh = round(float(ekwh) * 1000, 2)
    ekwh = str(ekwh)

    # Weitere Zählerdaten für die Statusseite (PowerFaktor, Spannung und Strom)
    # Powerfaktor ist nach dem Firmwareupgrade auf EM2 00.01.03.06 (04-2021) nicht mehr in der values.xml daher fix auf 1
    if newversion == False:
        evupf1 = 1
        evupf2 = 1
        evupf3 = 1
    else:
        evupf1 = get_xml_text(root, "value", "id", var_evupf1)
        evupf2 = get_xml_text(root, "value", "id", var_evupf2)
        evupf3 = get_xml_text(root, "value", "id", var_evupf3)

    evuv1 = get_xml_text(root, "value", "id", var_evuv1)
    evuv2 = get_xml_text(root, "value", "id", var_evuv2)
    evuv3 = get_xml_text(root, "value", "id", var_evuv3)
    bezuga1 = get_xml_text(root, "value", "id", var_bezuga1)
    bezuga2 = get_xml_text(root, "value", "id", var_bezuga2)
    bezuga3 = get_xml_text(root, "value", "id", var_bezuga3)
    # Prüfen ob Werte gültig
    regex = '^[-+]?[0-9]+\.?[0-9]*$'
    if re.search(regex, wattbezug) == None:
        with open("/var/www/html/openWB/ramdisk/wattbezug", "r") as f:
            wattbezug = int(f.read())

    # Ausgabe
    with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
        f.write(str(wattbezug))
    with open("/var/www/html/openWB/ramdisk/bezugw1", "w") as f:
        f.write(str(wattbezug1))
    with open("/var/www/html/openWB/ramdisk/bezugw2", "w") as f:
        f.write(str(wattbezug2))
    with open("/var/www/html/openWB/ramdisk/bezugw3", "w") as f:
        f.write(str(wattbezug3))
    with open("/var/www/html/openWB/ramdisk/bezugkwh", "w") as f:
        f.write(str(ikwh))
    with open("/var/www/html/openWB/ramdisk/einspeisungkwh", "w") as f:
        f.write(str(ekwh))
    with open("/var/www/html/openWB/ramdisk/evupf1", "w") as f:
        f.write(str(evupf1))
    with open("/var/www/html/openWB/ramdisk/evupf2", "w") as f:
        f.write(str(evupf2))
    with open("/var/www/html/openWB/ramdisk/evupf3", "w") as f:
        f.write(str(evupf3))
    with open("/var/www/html/openWB/ramdisk/evuv1", "w") as f:
        f.write(str(evuv1))
    with open("/var/www/html/openWB/ramdisk/evuv2", "w") as f:
        f.write(str(evuv2))
    with open("/var/www/html/openWB/ramdisk/evuv3", "w") as f:
        f.write(str(evuv3))
    with open("/var/www/html/openWB/ramdisk/bezuga1", "w") as f:
        f.write(str(bezuga1))
    with open("/var/www/html/openWB/ramdisk/bezuga2", "w") as f:
        f.write(str(bezuga2))
    with open("/var/www/html/openWB/ramdisk/bezuga3", "w") as f:
        f.write(str(bezuga3))


    log.debug('Watt: ' + str(wattbezug))
    log.debug('Einspeisung: ' + str(ekwh))
    log.debug('Bezug: ' + str(ikwh))
    log.debug('Leistung L1: ' + str(wattbezug1))
    log.debug('Leistung L2: ' + str(wattbezug2))
    log.debug('Leistung L3: ' + str(wattbezug3))
    log.debug('Power Faktor L1: ' + str(evupf1))
    log.debug('Power Faktor L2: ' + str(evupf2))
    log.debug('Power Faktor L3: ' + str(evupf3))
    log.debug('Spannung L1: ' + str(evuv1))
    log.debug('Spannung L2: ' + str(evuv2))
    log.debug('Spannung L3: ' + str(evuv3))
    log.debug('Strom L1: ' + str(bezuga1))
    log.debug('Strom L2: ' + str(bezuga2))
    log.debug('Strom L3: ' + str(bezuga3))

def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)

