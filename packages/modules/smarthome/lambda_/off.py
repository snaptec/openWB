#!/usr/bin/python3
import sys
import os
import struct
import codecs
import logging
from smarthome.smartlog import initlog
from pymodbus.client.sync import ModbusTcpClient
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
uberschussvz = str(sys.argv[4])
initlog("lambda", devicenumber)
log = logging.getLogger("lambda")
if (uberschussvz == 'UN'):
    uberschuss = uberschuss * -1
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
# standard
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
log.info(' off.py devicenr %d ipadr %s ueberschuss %6d try to connect (modbus)'
         % (devicenumber, ipadr, uberschuss))
client = ModbusTcpClient(ipadr, port=502)
start = 103
resp = client.read_holding_registers(start, 2)
value1 = resp.registers[0]
all = format(value1, '04x')
aktpower = int(struct.unpack('>h', codecs.decode(all, 'hex'))[0])
log.info(' off.py devicenr %d ipadr %s Akt Leistung  %6d'
         % (devicenumber, ipadr, aktpower))
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
# wenn vorher pvmodus an, dann watt.py
# signaliseren einmalig 0 ueberschuss zu schicken
if pvmodus == 1:
    pvmodus = 99
with open(file_stringpv, 'w') as f:
    f.write(str(pvmodus))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
