#!/usr/bin/python3
import sys
import os
import logging
from smarthome.smartlog import initlog
from smarthome.smartret import writeret
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
initlog("stiebel", devicenumber)
log = logging.getLogger("stiebel")
file_stringpv = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
# pv modus
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
aktpower = 0
powerc = 0
answer = '{"power":' + str(aktpower) + ',"powerc":' + str(powerc) + ',"on":' + str(pvmodus) + '}'
writeret(answer, devicenumber)
