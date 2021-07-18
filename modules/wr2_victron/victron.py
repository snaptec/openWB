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
mid = int(sys.argv[2])

client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()

# mppt watt
resp= client.read_holding_registers(789,1,unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
mpp_watt1 = str(decoder.decode_16bit_uint())
mpp_watt2 = int(mpp_watt1) / 10 * -1
f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
f.write(str(mpp_watt2))
f.close()

client.close()
