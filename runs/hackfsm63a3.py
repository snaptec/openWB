#!/usr/bin/python
import sys
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

# Modbus RTU port and id of the Fronius Smart Meter 63A-3
if len(sys.argv) == 1:
    mb_port = '/dev/ttyUSB1'
    mb_id = 3
    start_address = 4096
    number_of_addresses = 80
    #addresses_to_be_excluded = []
    addresses_to_be_excluded = range(4096,4107,2) + range(4110,4121,2) \
                               + range(4124,4127,2) + range(4134,4139,2) \
                               + range(4140,4145,2) + range(4158,4175,2)
else:
    print(str(sys.argv))
    mb_port = str(sys.argv[1])
    mb_id = int(sys.argv[2])
    start_address = int(sys.argv[3])
    number_of_addresses = int(sys.argv[4])
    addresses_to_be_excluded = []

client = ModbusSerialClient(method = "rtu", port=mb_port, baudrate=9600,
        stopbits=1, bytesize=8, timeout=1)

#client.connect()

for current_address in range(start_address, start_address + number_of_addresses + 1, 2):
    if current_address in addresses_to_be_excluded:
        continue
    result = client.read_holding_registers(current_address, 2, unit=mb_id)
    if result.isError():
        print('Address {}: <not working>'.format(current_address))
    else:
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers,
                                                     byteorder=Endian.Big,
                                                     wordorder=Endian.Big)
        decoded_value_raw = decoder.decode_32bit_uint()
        decoded_value_str = '{}'.format(decoded_value_raw)
        print('Address {}: {}'.format(current_address, decoded_value_str))
 
#client.close()
