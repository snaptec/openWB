#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

seradd = str(sys.argv[1])
if "dev" in seradd:
    from pymodbus.client.sync import ModbusSerialClient
    client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
                                        stopbits=1, bytesize=8, timeout=1)
else:
    from pymodbus.client.sync import ModbusTcpClient
    client = ModbusTcpClient('192.168.193.31', port=8899)

sdmid = int(85)
time.sleep(0.1)
#reg bat volt
resp = client.read_holding_registers(0x0010,2, unit=sdmid)
voltr = resp.registers[0]
time.sleep(0.1)
#reg battamp
resp = client.read_holding_registers(0x0011,2, unit=sdmid)
value1 = resp.registers[0]
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
value1 = int(decoder.decode_16bit_int())
volt = voltr * 0.02
amp = value1 * 0.1
battwatt = int(volt * amp * -1)
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(battwatt))
f.close()
time.sleep(0.1)
#reg batt soc
resp = client.read_holding_registers(0x002D,2, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
w2 = int(decoder.decode_16bit_int())
socf = int(w2 * 0.1)
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(socf))
f.close()
time.sleep(0.1)
resp = client.read_holding_registers(0x0030,2, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
pvw = int(decoder.decode_16bit_int())
time.sleep(0.1)
resp = client.read_holding_registers(0x0033,2, unit=sdmid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers,byteorder=Endian.Big,wordorder=Endian.Big)
pvw2 = int(decoder.decode_16bit_int())
pvwg = int((pvw + pvw2) * -1)
oldpv = open('/var/www/html/openWB/ramdisk/pvwatt', 'r')
oldpv = int(oldpv.read())
newpv = int(pvwg + oldpv)
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(newpv))
f.close()



