#!/usr/bin/env python3

import re
import requests
import sys
import traceback

multifems = str(sys.argv[1])
femskacopw = str(sys.argv[2])
femsip = str(sys.argv[3])


def get_value(url_ending, file=None):
    try:
        response = requests.get("http://x:"+femskacopw+"@"+femsip+":8084/rest/channel/"+url_ending).json()
        value = response["value"]
        if file != None:
            if file == "speichersoc":
                if re.search('^[-+]?[0-9]+\.?[0-9]*$', value) == None:
                    value = "0"
            with open("/var/www/html/openWB/ramdisk/"+file, "") as f:
                f.write(str(value))
        else:
            return value
    except:
        traceback.print_exc()


if multifems == "0":
    get_value("ess0/Soc", "speichersoc")
    get_value("ess0/ActiveChargeEnergy", "speicherikwh")
    get_value("ess0/ActiveDischargeEnergy", "speicherekwh")
else:
    get_value("ess2/Soc", "speichersoc")
    get_value("ess2/ActiveChargeEnergy", "speicherikwh")
    get_value("ess2/ActiveDischargeEnergy", "speicherekwh")

grid = get_value("_sum/GridActivePower")
pv = get_value("_sum/ProductionActivePower")
haus = get_value("_sum/ConsumptionActivePower")

leistung = grid + pv - haus

ra = '^[-+]?[0-9]+\.?[0-9]*$'
if re.search(ra, leistung) == None:
    leistung = "0"
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(leistung))
