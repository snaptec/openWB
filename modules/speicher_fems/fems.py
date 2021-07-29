#!/usr/bin/env python3

import json
import re
import requests
import sys

multifems = str(sys.argv[1])
femskacopw = str(sys.argv[2])
femsip = str(sys.argv[3])


def get_value(url_ending, file=None):
    response = requests.get("http://x:"+femskacopw+"@"+femsip+":8084/rest/channel/"+url_ending)
    response = json.loads(response)
    value = response["value"]
    if file != None:
        if file == "speichersoc":
            if re.search('^[-+]?[0-9]+\.?[0-9]*$', value) == None:
                value = "0"
        with open("/var/www/html/openWB/ramdisk/"+file, "") as f:
            f.write(str(value))
    else:
        return value


if multifems == "0":
    get_value("speichersoc", "ess0/Soc")
    get_value("speicherikwh", "ess0/ActiveChargeEnergy")
    get_value("speicherekwh", "ess0/ActiveDischargeEnergy")
else:
    get_value("speichersoc", "ess2/Soc")
    get_value("speicherikwh", "ess2/ActiveChargeEnergy")
    get_value("speicherekwh", "ess2/ActiveDischargeEnergy")

grid = get_value("_sum/GridActivePower")
pv = get_value("_sum/ProductionActivePower")
haus = get_value("_sum/ConsumptionActivePower")

leistung = grid + pv - haus

ra = '^[-+]?[0-9]+\.?[0-9]*$'
if re.search(ra, leistung) == None:
    leistung = "0"
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(leistung))
