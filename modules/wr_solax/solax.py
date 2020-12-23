#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import struct
import binascii


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
    val =  addr
    if val > 32767:
        val -= 65535
    return val

ipaddress = str(sys.argv[1])
client = ModbusTcpClient(ipaddress, port=502)


resp=client.read_input_registers(0, 114)

pv1 = unsigned16(resp, 10)
pv2 = unsigned16(resp, 11)


f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(pv1+pv2))
f.close()

pvall = unsigned32(resp,82) / 10   # yield today
f = open('/var/www/html/openWB/ramdisk/pvkwh', 'w')
f.write(str(pvall))
f.close()


