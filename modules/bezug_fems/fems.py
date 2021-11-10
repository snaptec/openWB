#!/usr/bin/env python3

import requests
import sys
import traceback

password = str(sys.argv[1])
ip_address = str(sys.argv[2])

def write_ramdisk(val, file):
    try:
        f = open('/var/www/html/openWB/ramdisk/'+file, 'w')
        f.write(str(val))
        f.close()
    except:
        traceback.print_exc()

# Grid meter values
try:
    response = requests.get('http://x:'+password+'@'+ip_address+':8084/rest/channel/meter0/(ActivePower.*|VoltageL.|Frequency)', timeout = 1).json()
except:
    traceback.print_exc()

v1, v2, v3 = 0, 0, 0
p1, p2, p3 = 0, 0, 0
for singleValue in response:
    address = singleValue['address']
    if (address == 'meter0/Frequency'):
        write_ramdisk(singleValue['value'], 'evuhz')
    elif (address == 'meter0/ActivePower'):
        write_ramdisk(singleValue['value'], 'wattbezug')
    elif (address == 'meter0/ActivePowerL1'):
        write_ramdisk(singleValue['value'], 'bezugw1')
        p1 = singleValue['value']
    elif (address == 'meter0/ActivePowerL2'):
        write_ramdisk(singleValue['value'], 'bezugw2')
        p2 = singleValue['value']
    elif (address == 'meter0/ActivePowerL3'):
        write_ramdisk(singleValue['value'], 'bezugw3')
        p3 = singleValue['value']
    elif (address == 'meter0/VoltageL1'):
        write_ramdisk(singleValue['value'], 'evuv1')
        v1 = singleValue['value']
    elif (address == 'meter0/VoltageL2'):
        write_ramdisk(singleValue['value'], 'evuv2')
        v2 = singleValue['value']
    elif (address == 'meter0/VoltageL3'):
        write_ramdisk(singleValue['value'], 'evuv3')
        v3 = singleValue['value']

if (v1 != 0):
    a1 = p1 / v1
    write_ramdisk(a1, 'bezuga1')
if (v2 != 0):
    a2 = p2 / v2
    write_ramdisk(a2, 'bezuga2')
if (v3 != 0):
    a3 = p3 / v3
    write_ramdisk(a3, 'bezuga3')

# Grid total energy sums
try:
    response = requests.get('http://x:'+password+'@'+ip_address+':8084/rest/channel/_sum/Grid.+ActiveEnergy', timeout = 1).json()
except:
    traceback.print_exc()

for singleValue in response:
    address = singleValue['address']
    if (address == '_sum/GridBuyActiveEnergy'):
        write_ramdisk(singleValue['value'], 'bezugkwh')
    elif (address == '_sum/GridSellActiveEnergy'):
        write_ramdisk(singleValue['value'], 'einspeisungkwh')
