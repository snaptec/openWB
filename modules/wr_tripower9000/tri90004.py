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
ip3address = str(sys.argv[3])
ip4address = str(sys.argv[4])

client = ModbusTcpClient(ipaddress, port=502)
client2 = ModbusTcpClient(ip2address, port=502)
client3 = ModbusTcpClient(ip3address, port=502)
client4 = ModbusTcpClient(ip4address, port=502)

# pv watt
resp= client.read_holding_registers(30775,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr1w = int(struct.unpack('>i', all.decode('hex'))[0])

# pv Wh
resp= client.read_holding_registers(30529,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr1wh = int(struct.unpack('>i', all.decode('hex'))[0])

# pv watt
resp= client3.read_holding_registers(30775,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr3w = int(struct.unpack('>i', all.decode('hex'))[0])

# pv Wh
resp= client3.read_holding_registers(30529,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr3wh = int(struct.unpack('>i', all.decode('hex'))[0])

# pv watt
resp= client4.read_holding_registers(30775,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr4w = int(struct.unpack('>i', all.decode('hex'))[0])

# pv Wh
resp= client4.read_holding_registers(30529,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr4wh = int(struct.unpack('>i', all.decode('hex'))[0])

# pv watt
resp= client2.read_holding_registers(30775,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr2w = int(struct.unpack('>i', all.decode('hex'))[0])
final = wr1w + wr2w + wr3w + wr4w
if final < 0:
    final = 0
final = final * -1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()

# pv Wh
resp= client2.read_holding_registers(30529,2,unit=3)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value1, '04x') + format(value2, '04x')
wr2wh = int(struct.unpack('>i', all.decode('hex'))[0])
final = wr1wh + wr2wh + wr3wh + wr4wh
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(final))
f.close()
