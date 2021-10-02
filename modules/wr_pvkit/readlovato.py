#!/usr/bin/python
import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

##PV Kit Defaults
mbip='192.168.193.13'
mbport=8899
mbid=0x08
numpv = 1

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




# Counters
resp = client.read_input_registers(0x1a1f,2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalbezug1 = int(struct.unpack('>i', all.decode('hex'))[0])
resp = client.read_input_registers(0x1a21,2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalbezug2 = int(struct.unpack('>i', all.decode('hex'))[0])
if ( finalbezug1 > finalbezug2 ):
	finalbezug=finalbezug1
else:
	finalbezug=finalbezug2
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv) + 'kwh', 'w')

f.write(str(finalbezug))
f.close()

# phasen watt
resp = client.read_input_registers(0x0013,2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw1 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)

resp = client.read_input_registers(0x0015,2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw2 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
resp = client.read_input_registers(0x0017,2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
finalw3 = int(struct.unpack('>i', all.decode('hex'))[0] / 100)

finalw= finalw1 + finalw2 + finalw3
if ( finalw > 10):
	finalw=finalw*-1

# total watt
# resp = client.read_input_registers(0x0039,2, unit=mbid)
# all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
# finalw = int(struct.unpack('>i', all.decode('hex'))[0] / 100)
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv)+ 'watt', 'w')
f.write(str(finalw))
f.close()

# ampere l1
resp = client.read_input_registers(0x0007, 2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla1 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pva1', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv) + 'a1', 'w')
f.write(str(lla1))
f.close()

# ampere l2
resp = client.read_input_registers(0x0009, 2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla2 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pva2', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv) + 'a2', 'w')
f.write(str(lla2))
f.close()

# ampere l3
resp = client.read_input_registers(0x000b, 2, unit=mbid)
all = format(resp.registers[0], '04x') + format(resp.registers[1], '04x')
lla3 = float(struct.unpack('>i', all.decode('hex'))[0]) / 10000
if numpv == 1:
	f = open('/var/www/html/openWB/ramdisk/pva3', 'w')
else:
	f = open('/var/www/html/openWB/ramdisk/pv' + str(numpv) + 'a3', 'w')
f.write(str(lla3))
f.close()
