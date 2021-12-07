#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
import struct
import binascii
ipaddress = str(sys.argv[1])
ip2address = str(sys.argv[2])

from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])

client = ModbusTcpClient(ipaddress, port=502)

# battsoc
resp= client.read_holding_registers(1068,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')

sfinal = int(struct.unpack('>h', all.decode('hex'))[0]) 

#battleistung
resp= client.read_holding_registers(1066,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
lfinal = int(struct.unpack('>h', all.decode('hex'))[0]) 

if ip2address != 'none':
    client2 = ModbusTcpClient(ip2address, port=502)
    #battsoc
    resp= client2.read_holding_registers(1068,1,unit=1)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    final = int(struct.unpack('>h', all.decode('hex'))[0]) 
    sfinal=(sfinal+final)/2
    #battleistung
    resp= client2.read_holding_registers(1066,1,unit=1)
    value1 = resp.registers[0]
    all = format(value1, '04x')
    final = int(struct.unpack('>h', all.decode('hex'))[0]) 
    lfinal=lfinal+final

f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(sfinal))
f.close()
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(lfinal))
f.close()
