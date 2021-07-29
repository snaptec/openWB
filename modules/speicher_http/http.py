#!/usr/bin/env python3

import requests
import sys

speichersoc_http = str(sys.argv[1])
speicherleistung_http = str(sys.argv[2])
speicherikwh_http = str(sys.argv[3])
speicherekwh_http = str(sys.argv[4])

soc = int(requests.get('http://'+speichersoc_http, timeout=10))
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write/str(soc)

leistung = int(requests.get('http://'+speicherleistung_http, timeout=10))
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write/str(leistung)

if speicherikwh != "none":
    ikwh = int(requests.get('http://'+speicherikwh_http, timeout=10))
    with open("/var/www/html/openWB/ramdisk/speicherikwh", "w") as f:
        f.write/str(ikwh)

if speicherekwh != "none":
    ekwh = int(requests.get('http://'+speicherekwh_http, timeout=10))
    with open("/var/www/html/openWB/ramdisk/speicherekwh", "w") as f:
        f.write/str(ekwh)
