#!/usr/bin/python3
import sys
import os
import time
import json
import getopt
import socket
import struct
import codecs
import binascii
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S keba setcurr.py", named_tuple)
file_string= '/var/www/html/openWB/ramdisk/keba_setcurr.log'
if os.path.isfile(file_string):
    f = open( file_string , 'a')
else:
    f = open( file_string , 'w')
ipaddress=str(sys.argv[1])
newcurr=int(sys.argv[2])
client = ModbusTcpClient(ipaddress, port=502)
# maxcurr state 1100
resp= client.read_holding_registers(1100,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final = float( decoder.decode_32bit_uint()) / 1000
#value1 = resp.registers[0]
#value2 = resp.registers[1]
#all = format(value1, '04x') + format(value2, '04x')
#final = float(struct.unpack('>i', all.decode('hex'))[0]) / 1000
oldcurr = int("%.f" % final)
if (oldcurr != newcurr):
    if (newcurr == 0):
        # disable station
        print ('%s oldcurr %.f, newcurr %.f, ipadr %s disable station' % (time_string,oldcurr,newcurr,ipaddress),file=f)
        rq = client.write_register(5014,0,unit=255)
    else:
        if (oldcurr == 0):
            # enable station
            print ('%s oldcurr %.f, newcurr %.f, ipadr %s enable station' % (time_string,oldcurr,newcurr,ipaddress),file=f)
            rq = client.write_register(5014,1,unit=255)
        # setting new curr
        print ('%s oldcurr %.f, newcurr %.f, ipadr %s setting new curr' % (time_string,oldcurr,newcurr,ipaddress),file=f)
        newcurrt = newcurr * 1000
        rq = client.write_register(5004,newcurrt,unit=255)
f.close()
