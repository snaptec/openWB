#!/usr/bin/python3
import sys
# import os
# import time
# import getopt
# import socket
import struct
# import binascii
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient

ipadd = str(sys.argv[1])
client = ModbusTcpClient(ipadd, port=502)

#rq = client.read_holding_registers(0,8,unit=5)
#print(rq.registers)
modbusid = 1
readreg = 19026
reganzahl = 2

rq = client.read_holding_registers(readreg,reganzahl,unit=modbusid)
#print(rq.registers[0])
#print(rq.registers[1])
#print(rq.registers[2])
#print(rq.registers[3])

#value1 = rq.registers[0] 
#value2 = rq.registers[1] 
#all = format(value1, '04x') + format(value2, '04x')
#final = int(struct.unpack('>i', all.decode('hex'))[0])
#print(str(final))

FRegister_232 = BinaryPayloadDecoder.fromRegisters(rq.registers, byteorder=Endian.Big, wordorder=Endian.Little)
Current_phase_2_powermeter = round(FRegister_232.decode_32bit_float(),2)

voltage = struct.unpack('>f',struct.pack('>HH',*rq.registers))[0]
voltage2 = int(voltage)
f = open('/var/www/html/openWB/ramdisk/wattbezug', 'w')
f.write(str(voltage2))
f.close()
