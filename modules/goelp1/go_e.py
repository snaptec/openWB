#!/usr/bin/env python3

import json
import re
import requests
import sys


def get_value(file, field, scale=False):
    value = output["nrg"][field]
    if scale == True:
        value = int(value * 10)
    if re.search('^-?[0-9]+$', value) != None:
        with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
            f.write(str(value))


lp_num = str(sys.argv[1])
goeip = str(sys.argv[2])
goetimeout = str(sys.argv[3])

rekwh = '^[-+]?[0-9]+\.?[0-9]*$'

if lp_num == 1:
    file_ext = ""
elif lp_num == 2:
    file_ext = "s1"
    stat_ext = "s1"
elif lp_num == 3:
    file_ext = "s2"
    stat_ext = "lp3"

try:
    response = requests.get('http://'+goeip+'/status', timeout=goetimeout)
    output = json.loads(response)
    get_value("llaktuell"+file_ext, 11, True)
    get_value("lla"+file_ext+"1", 4, True)
    get_value("lla"+file_ext+"2", 5, True)
    get_value("lla"+file_ext+"3", 6, True)
    get_value("llv"+file_ext+"1", 0)
    get_value("llv"+file_ext+"2", 1)
    get_value("llv"+file_ext+"3", 2)
    llkwh = output["eto"]
    value = round((llkwh * 10), 3)
    if re.search(rekwh, llkwh) != None:
        with open("/var/www/html/openWB/ramdisk/llkwh"+file_ext, "w") as f:
            f.write(str(llkwh))

    if lp_num == 1:
        rfid = output["uby"]
        with open("/var/www/html/openWB/ramdisk/tmpgoelp1rfid", "r") as f:
            oldrfid = f.read()
        if rfid != oldrfid:
            with open("/var/www/html/openWB/ramdisk/readtag", "w") as f:
                f.write(str(rfid))
            with open("/var/www/html/openWB/ramdisk/tmpgoelp1rfid", "w") as f:
                f.write(str(rfid))
    # car status 1 Ladestation bereit, kein Auto
    # car status 2 Auto lädt
    # car status 3 Warte auf Fahrzeug
    # car status 4 Ladung beendet, Fahrzeug verbunden
    car = output["car"]
    if car == "1":
        with open("/var/www/html/openWB/ramdisk/plugstat"+stat_ext, "w") as f:
            f.write(str(0))
    else:
        with open("/var/www/html/openWB/ramdisk/plugstat"+stat_ext, "w") as f:
            f.write(str(1))
    if car == "2":
        with open("/var/www/html/openWB/ramdisk/chargestat"+stat_ext, "w") as f:
            f.write(str(1))
    else:
        with open("/var/www/html/openWB/ramdisk/chargestat"+stat_ext, "w") as f:
            f.write(str(0))
except requests.exceptions.RequestException as e:
    pass
