#!/usr/bin/python
import sys
import os
import time
import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient('192.168.193.19', port=8899)
#from pymodbus.transaction import ModbusRtuFramer
#client = ModbusTcpClient('192.168.0.7', port=8899, framer=ModbusRtuFramer)




resp = client.read_input_registers(0x0048,2, unit=9)
vwh = struct.unpack('>f',struct.pack('>HH',*resp.registers))
ikwh = float("%.3f" % vwh[0]) * int(1000)
f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
f.write(str(ikwh))
f.close()

#total watt
resp = client.read_input_registers(0x000C,2, unit=9)
watt = struct.unpack('>f',struct.pack('>HH',*resp.registers))
watt = int(watt[0])
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(watt))
f.close()



#export kwh
resp = client.read_input_registers(0x004a,2, unit=9)
vwhe = struct.unpack('>f',struct.pack('>HH',*resp.registers))
ekwh = float("%.3f" % vwhe[0]) * int(1000)
f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
f.write(str(ekwh))
f.close()


