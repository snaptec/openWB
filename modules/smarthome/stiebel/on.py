#!/usr/bin/python3
import sys
from pymodbus.client.sync import ModbusTcpClient
import logging
from smarthome.smartlog import initlog
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
initlog("stiebel", devicenumber)
log = logging.getLogger("stiebel")
file_stringpv = '/var/www/html/openWB/ramdisk/smarthome_device_' + str(devicenumber) + '_pv'
log.info('on devicenr %d ipadr %s ueberschuss %6d try to connect (modbus)' % (devicenumber, ipadr, uberschuss))
client = ModbusTcpClient(ipadr, port=502)
# activate switch one (manual 4002)
rq = client.write_register(4001, 1, unit=1)
log.info('on devicenr %d ipadr %s ' % (devicenumber, ipadr))
with open(file_stringpv, 'w') as f:
    f.write(str(1))
