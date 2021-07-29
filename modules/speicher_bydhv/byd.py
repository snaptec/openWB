#!/usr/bin/env python3

import re
import requests
import sys

bydhvip = str(sys.argv[1])
bydhvuser = str(sys.argv[2])
bydhvpass = str(sys.argv[3])

response = requests.get('http://'+bydhvip+'/asp/RunData.asp', auth=(bydhvuser, bydhvpass))
response = response.split("\n")
for line in response:
    if "SOC:" in response[line]:
        response = response[line:line+2]
        break
response = response.replace("%", "")
group = re.search("^.*value=$", response).group()
soc = response.replace(group, "")
with open("/var/www/html/openWB/ramdisk/speichersoc", "w") as f:
    f.write(str(soc))

response = requests.get('http://'+bydhvip+'/asp/Home.asp', auth=(bydhvuser, bydhvpass))
response = response.split("\n")
for line in response:
    if "Power:" in response[line]:
        response = response[line:line+2]
        break
response = response.replace(">", "")
group = re.search("^.*value=$", response).group()
speicherleistung = response.replace(group, "")
speicherleistung = int(speicherleistung*1000)
with open("/var/www/html/openWB/ramdisk/speicherleistung", "w") as f:
    f.write(str(speicherleistung))
