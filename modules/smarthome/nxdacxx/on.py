#!/usr/bin/python3
import sys
import logging
from smarthome.smartlog import initlog
from pymodbus.client.sync import ModbusTcpClient
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
port = int(sys.argv[4])
dactyp = int(sys.argv[5])
initlog("DAC", devicenumber)
log = logging.getLogger("DAC")
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
log.info('on devicenr %d ipadr %s dactyp %d' % (devicenumber, ipadr, dactyp))
if dactyp == 2:
    client = ModbusTcpClient(ipadr, port=port)
    # DO1 einschalten um SGready zu aktivieren
    rq = client.write_coil(0, True, unit=1)
pvmodus = 1
with open(file_stringpv, 'w') as f:
    f.write(str(pvmodus))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
count5 = 999
with open(file_stringcount5, 'w') as f:
    f.write(str(count5))
