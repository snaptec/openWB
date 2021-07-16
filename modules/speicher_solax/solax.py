#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient

def unsigned16(result, addr):
    return result.registers[addr]

def signed16(result, addr):
    val = result.registers[addr]
    if val > 32767:
        val -= 65535
    return val

ipaddress = str(sys.argv[1])

client = ModbusTcpClient(ipaddress, port=502)

resp=client.read_input_registers(0, 114)

# Batterie Power
value1 = signed16(resp, 22)
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(value1))
f.close()

# Batterieladezustand
value2 = unsigned16(resp, 28 )
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(value2))
f.close()
