#!/usr/bin/python3
import sys
import struct
from pymodbus.client.sync import ModbusTcpClient
import logging
from smarthome.smartlog import initlog
devicenumber = int(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
try:
    navvers = str(sys.argv[4])
except Exception:
    navvers = "2"
initlog("idm", devicenumber)
log = logging.getLogger("idm")
# standard
# lesen
# own log
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
log.info("devicenr %d ipadr %s ueberschuss %6d try to connect (modbus)"
         % (devicenumber, ipadr, uberschuss))
client = ModbusTcpClient(ipadr, port=502)
start = 4122
if navvers == "2":
    rr = client.read_input_registers(start, 2, unit=1)
else:
    rr = client.read_holding_registers(start, 2, unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
lkw = float(struct.unpack('>f', raw)[0])
aktpower = int(lkw*1000)
log.info("devicenr %d ipadr %s Akt Leistung  %6d " %
         (devicenumber, ipadr, aktpower))
with open(file_stringpv, 'w') as f:
    f.write(str(1))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
