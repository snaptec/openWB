#!/usr/bin/env python3

import json
import requests
import sys

password = str(sys.argv[1])
ip_address = str(sys.argv[2])

def get_value(url, file):
    response = requests.get(url, timeout = 2).json()
    val = response["value"]
    f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
    f.write(str(val))
    f.close()

get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/ActivePower', 'wattbezug')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/_sum/GridBuyActiveEnergy', 'bezugkwh')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/_sum/GridSellActiveEnergy', 'einspeisungkwh')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/VoltageL1', 'evuv1')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/VoltageL2', 'evuv2')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/VoltageL3', 'evuv3')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/CurrentL1', 'bezuga1')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/CurrentL2', 'bezuga2')
get_value('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/CurrentL3', 'bezuga3')
