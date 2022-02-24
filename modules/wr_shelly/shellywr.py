#!/usr/bin/python3
import json
import urllib.request
from typing import List

from helpermodules.cli import run_using_positional_cli_args


def totalPowerFromShellyJson(answer):
    if 'meters' in answer:
        meters = answer['meters']  # shelly
    else:
        meters = answer['emeters']  # shellyEM & shelly3EM
    total = 0
    # shellyEM has one meter, shelly3EM has three meters:
    for meter in meters:
        total = total + meter['power']
    return int(total)


def update(ipadr: str, fname: str):
    aktpower = 0

    # Versuche Daten von Shelly abzurufen.
    answer = json.loads(str(urllib.request.urlopen("http://"+str(ipadr)+"/status", timeout=3).read().decode("utf-8")))
    f = open('/var/www/html/openWB/ramdisk/shelly_wr_ret.' + str(ipadr), 'w')
    f.write(str(answer))
    f.close()
    # Versuche Werte aus der Antwort zu extrahieren.
    try:
        aktpower = totalPowerFromShellyJson(answer) * -1
    except:
        aktpower = 0

    f1 = open('/var/www/html/openWB/ramdisk/' + str(fname), 'w')
    f1.write(str(aktpower))
    f1.close()


def main(argv: List[str]):
    run_using_positional_cli_args(update, argv)
