#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import struct
# import binascii
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.factory import ClientDecoder

def unsigned32(result, addr):
   low  = result.registers[addr]
   high = result.registers[addr + 1]
   val = low +( high << 16)
   return val

def unsigned16 (result, addr):
    return result.registers[addr]

def signed16(result, addr):
    val = result.registers[addr]
    if val > 32767:
        val -= 65535
    return val

def signed32(result, addr):
    val = unsigned32(result, addr)
    if val > 2147483647:
        val -=  4294967295
    return val

ipaddress = str(sys.argv[1])
client = ModbusTcpClient(ipaddress, port=502)

resp=client.read_input_registers(0, 114)

value = signed32(resp, 70)
# for SolaX negative means get power from grid
value = -value

f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(value))
f.close()

frequenz = unsigned16(resp,7) / 100
print (frequenz)
f = open('/var/www/html/openWB/ramdisk/evuhz', 'w')
f.write(str(frequenz))
f.close()

consumed = unsigned32(resp,74) / 100
print (consumed)
f = open('/var/www/html/openWB/ramdisk/bezugkwh', 'w')
f.write(str(consumed))
f.close()

einspeisung = unsigned32(resp,72) / 100
f = open('/var/www/html/openWB/ramdisk/einspeisungkwh', 'w')
f.write(str(einspeisung))
f.close()
