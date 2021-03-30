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


resp=client.read_input_registers(10, 2)
pv1 = unsigned16(resp, 0)
pv2 = unsigned16(resp, 1)
f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
f.write(str( (pv1 + pv2) * -1   ) )  # Erzeugung negativ  
f.close()

resp=client.read_input_registers(80, 4)
pvall = unsigned32(resp,2)       # yield overall
f = open('/var/www/html/openWB/ramdisk/pv2kwh', 'w')
f.write(str(pvall))
f.close()
f = open('/var/www/html/openWB/ramdisk/pv2kwhk', 'w')
f.write(str(pvall / 1000))
f.close()

client.close()
