#!/usr/bin/python
import sys
# import os
import time
# import getopt
# import socket
# import ConfigParser
import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])
idaddress = int(sys.argv[2])
client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()
time.sleep(7)
# resp= client.read_holding_registers(32066,1,unit=1)
# value1 = resp.registers[0]
# print(str(value1))
# all = format(value1, '04x') + format(value2, '04x')
# final = int(struct.unpack('>i', all.decode('hex'))[0])*-1
# f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
# f.write(str(final))
# f.close()
# print(str(final))


#pv watt
resp= client.read_holding_registers(32064,2,unit=idaddress)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])*-1
if final > -65536:
    f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
    f.write(str(final))
    f.close()

# wattbezug
try:
    resp= client.read_holding_registers(37113,2,unit=idaddress)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])*-1
    f = open('/var/www/html/openWB/ramdisk/huaweibezugwatt', 'w')
    f.write(str(final))
    f.close()
except:
    pass
#evu phasenleistung
try:
    resp= client.read_holding_registers(37107,2,unit=idaddress)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])/100*-1
    f = open('/var/www/html/openWB/ramdisk/huaweievua1', 'w')
    f.write(str(final))
    f.close()
    resp= client.read_holding_registers(37109,2,unit=idaddress)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])/100*-1
    f = open('/var/www/html/openWB/ramdisk/huaweievua2', 'w')
    f.write(str(final))
    f.close()
    resp= client.read_holding_registers(37111,2,unit=idaddress)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])/100*-1
    f = open('/var/www/html/openWB/ramdisk/huaweievua3', 'w')
    f.write(str(final))
    f.close()
except:
    pass
try: 
    resp= client.read_holding_registers(37001,2,unit=idaddress)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    finalb1 = int(struct.unpack('>i', all.decode('hex'))[0])

except:
    finalb1=0
    pass
try: 
    resp= client.read_holding_registers(37743,2,unit=idaddress)
    value1 = resp.registers[0]
    value2 = resp.registers[1]
    all = format(value1, '04x') + format(value2, '04x')
    finalb2 = int(struct.unpack('>i', all.decode('hex'))[0])

except:
    finalb2=0
    pass
finalb=finalb1+finalb2
f = open('/var/www/html/openWB/ramdisk/huaweispeicherleistung', 'w')
f.write(str(finalb))
f.close()

try:
    resp= client.read_holding_registers(37760,2,unit=idaddress)
    value1 = int(resp.registers[0])/10
    all = format(value1, '04x') + format(value2, '04x')
    final = int(struct.unpack('>i', all.decode('hex'))[0])/10
    f = open('/var/www/html/openWB/ramdisk/huaweispeichersoc', 'w')
    f.write(str(value1))
    f.close()
except:
    pass
