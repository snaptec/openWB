#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
ipaddress 		= str(sys.argv[1])	#IP-Address Modbus Gateway
xtcount 		= int(sys.argv[2]) 	#studer_xt (count XT* Devices)
vccount 		= int(sys.argv[3])	#studer_vc (count MPPT Devices)
studervctype 	= str(sys.argv[4])	#studer_vc_type (MPPT type VS or VT)

from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()

def func_pvwatt():
#loop for pvwatt
	if studervctype == 'VS':
		mb_unit = int(40)
		mb_register = int(20)
	elif studervctype == 'VT':
		mb_unit=int(20)
		mb_register=int(8)
	pvwatt = 0
	i = 1
	while i < vccount+1:
		mb_unit_dev=mb_unit+i
		request = client.read_input_registers(mb_register,2,unit=mb_unit_dev)
		if request.isError():
			# handle error, log?
			print('Modbus Error:', request)
		else:
			result = request.registers
		decoder = BinaryPayloadDecoder.fromRegisters(result, byteorder=Endian.Big)
		pvwatt = pvwatt+decoder.decode_32bit_float() # type: float
		i += 1
	
	pvwatt=int(round(pvwatt*1000*-1,0)) #openWB need the values as negative Values in W
	#print (pvwatt)
	f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
	f.write(str(pvwatt))
	f.close()

func_pvwatt()

client.close()

