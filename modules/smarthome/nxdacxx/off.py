#!/usr/bin/python3
import sys
import os
import logging
from smarthome.smartlog import initlog
from pymodbus.client.sync import ModbusTcpClient
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
port = int(sys.argv[4])
dactyp = int(sys.argv[5])
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
initlog("DAC", devicenumber)
log = logging.getLogger("DAC")
log.info('off devicenr %d ipadr %s dactyp %d' % (devicenumber, ipadr, dactyp))
if dactyp == 2:
    client = ModbusTcpClient(ipadr, port=port)
    # DO1 ausschalten um SGready zu sperren
    rq = client.write_coil(0, False, unit=1)
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
#  wenn vorher pvmodus an, dann watt.py signaliseren einmalig 0
#  ueberschuss zu schicken
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
