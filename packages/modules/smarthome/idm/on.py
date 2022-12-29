#!/usr/bin/python3
import sys
import os
import time
import struct
from pymodbus.client.sync import ModbusTcpClient
named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S idm on.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
try:
    navvers = str(sys.argv[4])
except Exception:
    navvers = "2"
# standard
# lesen
# own log
file_string = bp + str(devicenumber) + '_idm.log'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
if os.path.isfile(file_string):
    pass
else:
    with open(file_string, 'w') as f:
        print('IDM start log', file=f)
with open(file_string, 'a') as f:
    print('%s devicenr %s ipadr %s ueberschuss %6d try to connect (modbus)'
          % (time_string, devicenumber, ipadr, uberschuss), file=f)
client = ModbusTcpClient(ipadr, port=502)
start = 4122
if navvers == "2":
    rr = client.read_input_registers(start, 2, unit=1)
else:
    rr = client.read_holding_registers(start, 2, unit=1)
raw = struct.pack('>HH', rr.getRegister(1), rr.getRegister(0))
lkw = float(struct.unpack('>f', raw)[0])
aktpower = int(lkw*1000)
with open(file_string, 'a') as f:
    print('%s devicenr %s ipadr %s Akt Leistung  %6d ' %
          (time_string, devicenumber, ipadr, aktpower), file=f)
with open(file_stringpv, 'w') as f:
    f.write(str(1))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
