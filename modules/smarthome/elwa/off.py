#!/usr/bin/python3
import sys
import logging
from smarthome.smartlog import initlog
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
# standard
initlog("elwa", devicenumber)
log = logging.getLogger("elwa")
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
log.info("off devicenr %d ipadr %s ueberschuss %6d" %
         (devicenumber, ipadr, uberschuss))
with open(file_stringpv, 'w') as f:
    f.write(str(0))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
