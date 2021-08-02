#!/usr/bin/env python3

import re
import requests
from requests.auth import HTTPDigestAuth
import sys

wrsunwavesip = str(sys.argv[1])
wrsunwavespw = str(sys.argv[2])

params = (('CAN', '1'),)
variable = requests.get("http://"+wrsunwavesip+"/data/ajax.txt", params=params, auth=HTTPDigestAuth("customer", wrsunwavespw))
variable.encoding = 'utf-8'
variable = variable.text

count = 0

for v in variable:
    if count == 1:
        pvwatt = re.search('^[0-9]+$', v).group()
        pvwatt = pvwatt*-1
        with open("/var/www/html/openWB/ramdisk/pvwatt", "w") as f:
            f.write(str(pvwatt))
    if count == 16:
        with open("/var/www/html/openWB/ramdisk/pvkwh", "w") as f:
            f.write(str(v*1000))
    count = count+1
