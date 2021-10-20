#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])
ip2address = str(sys.argv[2])

client = ModbusTcpClient(ipaddress, port=502)
client2 = ModbusTcpClient(ip2address, port=502) #Zweites E3DC

# battsoc
resp= client.read_holding_registers(40082,1,unit=1)
resp2= client2.read_holding_registers(40082,1,unit=1) #Zweites E3DC
value1 = resp.registers[0]
value2 = resp2.registers[0]
all1 = format(value1, '04x')
all2 = format(value2, '04x')
final1 = int(struct.unpack('>h', all1.decode('hex'))[0]) 
final2 = int(struct.unpack('>h', all2.decode('hex'))[0]) 
final = (final1 + final2)/2
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(final))
f.close()
# print "hausverbrauch"
# resp= client.read_holding_registers(40071,2,unit=1)
# value1 = resp.registers[0]
# value2 = resp.registers[1]
# all = format(value2, '04x') + format(value1, '04x')
# final = int(struct.unpack('>i', all.decode('hex'))[0])
# print final
# pv punkt
resp= client.read_holding_registers(40067,2,unit=1)
resp2= client2.read_holding_registers(40067,2,unit=1) #Zweites E3DC
value1 = resp.registers[0]
value2 = resp.registers[1]
value3 = resp2.registers[0]
value4 = resp2.registers[1]
all1 = format(value2, '04x') + format(value1, '04x')
all2 = format(value4, '04x') + format(value3, '04x')
final1 = int(struct.unpack('>i', all1.decode('hex'))[0]) * -1
final2 = int(struct.unpack('>i', all2.decode('hex'))[0]) * -1
resp3= client.read_holding_registers(40075,2,unit=1) #BHKW
value5 = resp3.registers[0]
value6 = resp3.registers[1]
all3 = format(value6, '04x') + format(value5, '04x')
final3 = int(struct.unpack('>i', all3.decode('hex'))[0])
final = final1 + final2 + final3
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()
# battleistung
resp= client.read_holding_registers(40069,2,unit=1)
resp2= client2.read_holding_registers(40069,2,unit=1) #Zweites E3DC
value1 = resp.registers[0]
value2 = resp.registers[1]
value3 = resp2.registers[0]
value4 = resp2.registers[1]
all1 = format(value2, '04x') + format(value1, '04x')
all2 = format(value4, '04x') + format(value3, '04x')
final1 = int(struct.unpack('>i', all1.decode('hex'))[0])
final2 = int(struct.unpack('>i', all2.decode('hex'))[0])
final = final1 + final2
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()
