#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])
start = int(sys.argv[2])
length = int(sys.argv[3])
slaveid = int(sys.argv[4])
func = str(sys.argv[5])
named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S opentrace", named_tuple) 
client = ModbusTcpClient(ipaddress, port=502)
if func ==  "3":
   print('%s read input register ip %s start %6d len %3d id %s <br/> ' % (time_string,ipaddress,start,length,slaveid ))
   resp= client.read_input_registers(start,length,unit=slaveid)
else:
   print('%s read holding register ip %s start %6d len %3d id %s <br/> ' % (time_string,ipaddress,start,length,slaveid ))
   resp= client.read_holding_registers(start,length,unit=slaveid)
i= 0
while i < length:
   print ('%s start %6d  + %3d inhalt %6d %#4X <br/> ' % (time_string,start,i,resp.registers [i],resp.registers [i]
   ))
   i = i + 1