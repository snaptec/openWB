#!/usr/bin/python3
import sys
import os
import time
# import json
# import getopt
# import socket
# import struct
# import codecs
# import binascii
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S keba setcurr.py", named_tuple)

file_string= '/var/www/html/openWB/ramdisk/keba_setcurr.log'

def getstat(ip):
    # 1 enabled, 0 disable, 9 undef
    file_ip= '/var/www/html/openWB/ramdisk/keba_' + ip
    status = 9
    if os.path.isfile(file_ip):
        f = open(file_ip, 'r')
        status=int(f.read())
        f.close()
    return status

def setstat(ip,status):
    file_ip= '/var/www/html/openWB/ramdisk/keba_' + ip
    f1 = open(file_ip, 'w')
    f1.write(str(status))
    f1.close()

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
oldcurr = int("%.f" % final)

# cabel state 1004
resp= client.read_holding_registers(1004,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint())
plugs  = "%.f" % final2

# max supported curr 1110
resp= client.read_holding_registers(1110,2,unit=255)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
final2 = float( decoder.decode_32bit_uint()) / 1000
supcur = int("%.f" % final2)
if plugs == "7":
    if (oldcurr != newcurr):
        if (newcurr == 0):
            # disable station
            print ('%s oldcurr %d, newcurr %d, ipadr %s disable station' % (time_string,oldcurr,newcurr,ipaddress),file=f)
            rq = client.write_register(5014,0,unit=255)
            setstat(ipaddress,0)
        else:
            if (oldcurr == 0):
                #enable station
                print ('%s oldcurr %d, newcurr %d, ipadr %s enable station ' % (time_string,oldcurr,newcurr,ipaddress ),file=f)
                rq = client.write_register(5014,1,unit=255)
                setstat(ipaddress,1)
            # setting new curr
            print ('%s oldcurr %d, newcurr %d, hwlimit %d ipadr %s setting new curr' % (time_string,oldcurr,newcurr,supcur,ipaddress),file=f)
            newcurrt = newcurr * 1000
            rq = client.write_register(5004,newcurrt,unit=255)
else:
    status = getstat(ipaddress)
    if ((newcurr == 0) and (status != 0)) :
        # disable station
        print ('%s No car detected, ipadr %s disable station' % (time_string,ipaddress),file=f)
        rq = client.write_register(5014,0,unit=255)
        setstat(ipaddress,0)
    else:
        if ((newcurr > 0) and (status != 1)):
            #enable station
            print ('%s No car detected, ipadr %s enable station ' % (time_string,ipaddress ),file=f)
            rq = client.write_register(5014,1,unit=255)
            setstat(ipaddress,1)
f.close()
