#!/usr/bin/python3
import sys
import logging
import os
from smarthome.smartlog import initlog
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
# standard
initlog("askoheat", devicenumber)
log = logging.getLogger("askoheat")
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
log.info("off devicenr %d ipadr %s ueberschuss %6d" %
         (devicenumber, ipadr, uberschuss))
# wenn vorher pvmodus an, dann watt.py
# signaliseren einmalig 0 ueberschuss zu schicken
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
if pvmodus == 1:
    pvmodus = 99
with open(file_stringpv, 'w') as f:
    f.write(str(pvmodus))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
