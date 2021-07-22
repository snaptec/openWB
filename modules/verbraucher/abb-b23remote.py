#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
# import struct
# import binascii
import ctypes
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

#Args in var schreiben
verbrauchernr = str(sys.argv[1])
seradd = str(sys.argv[2])
ABBid = int(sys.argv[3])

client = ModbusClient(seradd, port=502, framer=ModbusRtuFramer)

response = client.read_holding_registers(address=0x5B00, count=28, unit=ABBid)

#Phase 1 A
al1 = ((response.registers[12] << 16) | response.registers[13]) / 10
al1string = "/var/www/html/openWB/ramdisk/verbraucher%s_a1" % (verbrauchernr)
f = open(al1string, 'w')
f.write(str(al1))
f.close()

#Phase 2 A
al2 = ((response.registers[14] << 16) | response.registers[15]) / 10
al2string = "/var/www/html/openWB/ramdisk/verbraucher%s_a2" % (verbrauchernr)
f = open(al2string, 'w')
f.write(str(al2))
f.close()

#Phase 3 A
al3 = ((response.registers[16] << 16) | response.registers[17]) / 10
al3string = "/var/www/html/openWB/ramdisk/verbraucher%s_a3" % (verbrauchernr)
f = open(al3string, 'w')
f.write(str(al3))
f.close()

#Phase 1 V
vl1 = ((response.registers[0] << 16) | response.registers[1]) / 10
vl1string = "/var/www/html/openWB/ramdisk/verbraucher%s_v1" % (verbrauchernr)
f = open(vl1string, 'w')
f.write(str(vl1))
f.close()

#Phase 2 V
vl2 = ((response.registers[2] << 16) | response.registers[3]) / 10
vl2string = "/var/www/html/openWB/ramdisk/verbraucher%s_v2" % (verbrauchernr)
f = open(vl2string, 'w')
f.write(str(vl2))
f.close()

#Phase 3 V
vl3 = ((response.registers[4] << 16) | response.registers[5]) / 10
vl3string = "/var/www/html/openWB/ramdisk/verbraucher%s_v3" % (verbrauchernr)
f = open(vl3string, 'w')
f.write(str(vl3))
f.close()

#KWH Total Export
# Not supported on ABB Steel Series Meters, broze and upwards may support export values
#Totoal Export
#response = client.read_holding_registers(address=0x5004, count=4, unit=ABBid)
whe = 0.0
# uncomment this line if you have a bronze or higher ABB meter
#whe = ((response.registers[0] << 32)|(response.registers[1] << 24)|(response.registers[2] << 16)|response.registers[3]) * 10.0
vwhestring = "/var/www/html/openWB/ramdisk/verbraucher%s_whe" % (verbrauchernr)
f = open(vwhestring, 'w')
f.write(str(whe))
f.close()

#Aktueller Verbrauch
#response = client.read_holding_registers(0x5B14,2, unit=ABBid)
watt = ((response.registers[20] << 16)| response.registers[21])
watt = ctypes.c_int32(watt).value / 100
wattstring = "/var/www/html/openWB/ramdisk/verbraucher%s_watt" % (verbrauchernr)
f = open(wattstring, 'w')
f.write(str(watt))
f.close()

#KWH Total Import
response = client.read_holding_registers(address=0x5000, count=4, unit=ABBid)
vwh = ((response.registers[0] << 32)|(response.registers[1] << 24)|(response.registers[2] << 16)|response.registers[3]) * 10.0
vwhstring = "/var/www/html/openWB/ramdisk/verbraucher%s_wh" % (verbrauchernr)
f = open(vwhstring, 'w')
f.write(str(vwh))
f.close()

client.close()
