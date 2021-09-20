#!/usr/bin/python
import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

mbip='192.168.193.13'
mbport=8899
mbid=8
numpv=1

#Check Argumentlist and replace Defaults if present
if len(sys.argv) >= 2:
	numpv=int(sys.argv[1])

if len(sys.argv) >= 3:
	mbip=str(sys.argv[2])

if len(sys.argv) >= 4:
	mbport=int(sys.argv[3])

if len(sys.argv) >= 5:
	mbid=int(sys.argv[4])


#client = ModbusTcpClient('192.168.193.13', port=8899)

client = ModbusTcpClient(mbip,port=mbport)
#client.host(mbip)
#client.port(mbport)
#client.unit_id(mbid)

resp = client.read_input_registers(0x0004,4, unit=mbid)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
ikwh = int(struct.unpack('>i', all.decode('hex'))[0]) 

# resp = client.read_input_registers(0x0004,2, unit=sdmid)
# ikwh = resp.registers[1]
ikwh = float(ikwh) * 10
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv) + 'kwh', 'w')
f.write(str(ikwh))
f.close()
pvkwhk= ikwh / 1000
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
f.write(str(pvkwhk))
f.close()

ikwhk = float(ikwh) / 1000
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pvkwhk', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv)+ 'kwhk', 'w')
f.write(str(ikwhk))
f.close()

resp = client.read_input_registers(0x0E,2, unit=mbid)
lla1 = resp.registers[1]
lla1 = float(lla1) / 100
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pva1', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv)+ 'a1', 'w')
f.write(str(lla1))
f.close()

resp = client.read_input_registers(0x10,2, unit=mbid)
lla2 = resp.registers[1]
lla2 = float(lla2) / 100
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pva2', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv) + 'a2', 'w')
f.write(str(lla2))
f.close()

resp = client.read_input_registers(0x12,2, unit=mbid)
lla3 = resp.registers[1]
lla3 = float(lla3) / 100
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pva3', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv)+ 'a3', 'w')
f.write(str(lla3))
f.close()

# total watt
resp = client.read_input_registers(0x26,2, unit=mbid)
value1 = resp.registers[0] 
value2 = resp.registers[1] 
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) / 100
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv)+ 'watt', 'w')
f.write(str(final))
f.close()
