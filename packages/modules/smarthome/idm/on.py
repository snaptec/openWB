#!/usr/bin/python3
import sys
import logging
from smarthome.smartlog import initlog
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
navvers = str(sys.argv[4])
initlog("idm", devicenumber)
log = logging.getLogger("idm")
# standard
# lesen
# own log
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
log.info("on.py devicenr %d ipadr %s ueberschuss %6d"
         % (devicenumber, ipadr, uberschuss))
with open(file_stringpv, 'w') as f:
    f.write(str(1))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
count5 = 999
with open(file_stringcount5, 'w') as f:
    f.write(str(count5))
