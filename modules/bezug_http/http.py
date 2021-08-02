#!/usr/bin/env python3
import re
import requests
import sys


def get_value(url, file):
    if url != "none":
        response = requests.get(url, timeout=5)
        response.encoding = 'utf-8'
        value = response.text.replace("\n", "")
        with open("/var/www/html/openWB/ramdisk/"+file, "w") as f:
            f.write(str(value))


bezug_http_w_url = str(sys.argv[1])
bezug_http_ikwh_url = str(sys.argv[2])
bezug_http_ekwh_url = str(sys.argv[3])
bezug_http_l1_url = str(sys.argv[4])
bezug_http_l2_url = str(sys.argv[5])
bezug_http_l3_url = str(sys.argv[6])

response = requests.get(bezug_http_w_url, timeout=10)
response.encoding = 'utf-8'
wattbezug = response.text.replace("\n", "")
regex = '^-?[0-9]+$'
if re.search(regex, wattbezug) == None:
    wattbezug = "0"
with open("/var/www/html/openWB/ramdisk/wattbezug", "w") as f:
    f.write(str(wattbezug))

get_value(bezug_http_ikwh_url, "bezugkwh")
get_value(bezug_http_ekwh_url, "einspeisungkwh")
get_value(bezug_http_l1_url, "bezuga1")
get_value(bezug_http_l2_url, "bezuga2")
get_value(bezug_http_l3_url, "bezuga3")
