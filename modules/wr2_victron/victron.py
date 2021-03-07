
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
from pymodbus.client.sync import ModbusTcpClient
ipaddress = str(sys.argv[1])
mid = int(sys.argv[2])
client = ModbusTcpClient(ipaddress, port=502)
connection = client.connect()

#PV-AC-coupled on output L1
resp = client.read_holding_registers(808, 1, unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
ac_output_L1_str = str(decoder.decode_16bit_uint())
ac_output_L1 = int(ac_output_L1_str) * -1

#PV-AC-coupled on output L2
resp = client.read_holding_registers(809, 1, unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
ac_output_L2_str = str(decoder.decode_16bit_uint())
ac_output_L2 = int(ac_output_L2_str) * -1

#PV-AC-coupled on output L3
resp = client.read_holding_registers(810, 1, unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
ac_output_L3_str = str(decoder.decode_16bit_uint())
ac_output_L3 = int(ac_output_L3_str) * -1

#PV-AC-coupled on input L1
resp = client.read_holding_registers(811, 1, unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
ac_input_L1_str = str(decoder.decode_16bit_uint())
ac_input_L1 = int(ac_input_L1_str) * -1

#PV-AC-coupled on input L2
resp = client.read_holding_registers(812, 1, unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
ac_input_L2_str = str(decoder.decode_16bit_uint())
ac_input_L2 = int(ac_input_L2_str) * -1

#PV-AC-coupled on input L3
resp = client.read_holding_registers(813, 1, unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
ac_input_L3_str = str(decoder.decode_16bit_uint())
ac_input_L3 = int(ac_input_L3_str) * -1

#System PV - DC-coupled power
resp = client.read_holding_registers(850, 1, unit=mid)
decoder = BinaryPayloadDecoder.fromRegisters(resp.registers, byteorder=Endian.Big, wordorder=Endian.Big)
dc_power_str = str(decoder.decode_16bit_uint())
dc_power = int(dc_power_str) * -1

watt = ac_output_L1 + ac_output_L2 + ac_output_L3 + ac_input_L1 + ac_input_L2 + ac_input_L3 + dc_power
f = open('/var/www/html/openWB/ramdisk/pv2watt', 'w')
f.write(str(watt))
f.close()

client.close()
