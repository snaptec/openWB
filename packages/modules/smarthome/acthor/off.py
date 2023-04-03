#!/usr/bin/python3
import sys
import os
import logging
from smarthome.smartlog import initlog
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
initlog("acthor", devicenumber)
log = logging.getLogger("acthor")
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
log.info("off devicenr %d ipadr %s ueberschuss %6d" %
         (devicenumber, ipadr, uberschuss))
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
#  wenn vorher pvmodus an, dann watt.py signalsieren einmalig 0 ueberschuss zu schicken
if pvmodus == 1:
    pvmodus = 99
with open(file_stringpv, 'w') as f:
    f.write(str(pvmodus))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
count5 = 999
with open(file_stringcount5, 'w') as f:
    f.write(str(count5))
