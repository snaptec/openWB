#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
# import ConfigParser
# import struct
# import binascii
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])

client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()

resp= client.read_holding_registers(811,1,unit=100)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
mpp1_watt1 = str(decoder.decode_16bit_uint())
mpp1_watt2 = int(mpp1_watt1) 
resp= client.read_holding_registers(812,1,unit=100)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
mpp2_watt1 = str(decoder.decode_16bit_uint())
mpp2_watt2 = int(mpp2_watt1) 
resp= client.read_holding_registers(813,1,unit=100)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
mpp3_watt1 = str(decoder.decode_16bit_uint())
mpp3_watt2 = int(mpp3_watt1) 
# mppt watt
resp= client.read_holding_registers(850,1,unit=100)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
mpp_watt1 = str(decoder.decode_16bit_uint())
mpp_watt2 = int(mpp_watt1)

final=(mpp1_watt2 + mpp2_watt2 + mpp3_watt2 + mpp_watt2) * -1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final))
f.close()

client.close()
