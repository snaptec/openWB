#!/usr/bin/env python3

import requests
import sys
import traceback

speichersoc_http = str(sys.argv[1])
speicherleistung_http = str(sys.argv[2])
speicherikwh_http = str(sys.argv[3])
speicherekwh_http = str(sys.argv[4])

try:
    response = requests.get(speichersoc_http, timeout=10)
    response.encoding = 'utf-8'
    soc = int(response.text.replace("\n", ""))
    with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
        f.write/str(soc)
except:
    traceback.print_exc()

try:
    response = requests.get(speicherleistung_http, timeout=10)
    response.encoding = 'utf-8'
    leistung = response.text.replace("\n", "")
    with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
        f.write/str(leistung)
except:
    traceback.print_exc()

if speicherikwh_http != "none":
    try:
        response = requests.get(speicherikwh_http, timeout=10)
        response.encoding = 'utf-8'
        ikwh = response.text.replace("\n", "")
        with open("/var/www/html/openWB/ramdisk/speicherikwh", "w") as f:
            f.write/str(ikwh)
    except:
        traceback.print_exc()

if speicherekwh_http != "none":
    try:
        response = requests.get(speicherekwh_http, timeout=10)
        response.encoding = 'utf-8'
        ekwh = response.text.replace("\n", "")
        with open("/var/www/html/openWB/ramdisk/speicherekwh", "w") as f:
            f.write/str(ekwh)
    except:
        traceback.print_exc()
