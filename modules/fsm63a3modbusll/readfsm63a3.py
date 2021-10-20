#!/usr/bin/python
import sys
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
# import math

# Set debug to "1" to enable debugging messages
debug = 0

# Check the given arguments
if debug == 1:
    print(str(sys.argv))

# Modbus RTU port and id of the Fronius Smart Meter 63A-3
mb_port = str(sys.argv[1])
mb_id = int(sys.argv[2])
# Path to the ramdisk
ramdiskpath = str(sys.argv[3])

# Definition of the values that will be requested
#            +-------------------------------------- Internal variable name (also used as ramdisk file name)
#            |           +-------------------------- Modbus Address
#            |           |     +-------------------- Multiplier to calculate the correct unit for openWB
#            |           |     |     +-------------- Precision (digits after the decimal separator)
#            |           |     |     |   +---------- Type (U16: unsigned int 16 bit, U32: unsigned int 32 bit, I32: signed int 32 bit)
#            |           |     |     |   |       +-- Description
#            |           |     |     |   |       |
values = (('llv1',      4096, 0.001, 2, 'U32', 'Voltage AC Phase 1 [0.001 * V]'),
          ('llv2',      4098, 0.001, 2, 'U32', 'Voltage AC Phase 2 [0.001 * V]'),
          ('llv3',      4100, 0.001, 2, 'U32', 'Voltage AC Phase 3 [0.001 * V]'),
          ('lla1',      4102, 0.001, 2, 'U32', 'Current AC Phase 1 [0.001 * A]'),
          ('lla2',      4104, 0.001, 2, 'U32', 'Current AC Phase 2 [0.001 * A]'),
          ('lla3',      4106, 0.001, 2, 'U32', 'Current AC Phase 3 [0.001 * A]'),
#          ('_llv12pp',  4110, 0.001, 2, 'U32', 'Voltage AC Phase to Phase 12 [0.001 * V]'),
#          ('_llv23pp',  4112, 0.001, 2, 'U32', 'Voltage AC Phase to Phase 23 [0.001 * V]'),
#          ('_llv31pp',  4114, 0.001, 2, 'U32', 'Voltage AC Phase to Phase 31 [0.001 * V]'),
          ('llaktuell', 4116, 0.01,  0, 'I32', 'Power Real P Sum [0.01 * W]'),
#          ('_ql123',    4118, 0.01,  0, 'I32', 'Power Reactive Q Sum [0.01 * VAr]'),
#          ('_sl123',    4120, 0.01,  0, 'U32', 'Power Apparent S Sum [0.01 * VA]'),
          ('llkwh',     4124, 0.001, 2, 'U32', 'Energy Real WAC Sum Consumed [0.001 * kWh]'),
#          ('_llvarh',   4126, 0.001, 2, 'U32', 'Energy Reactive VArAC Sum Consumed [0.001 * VArh]'),
#          ('_llpwh',    4128, 0.001, 2, 'U32', 'Energy Real WAC Sum Produced [0.001 * kWh]'),
#          ('_llpvarh',  4130, 0.001, 2, 'U32', 'Energy Reactive VArAC Sum Produced [0.001 * VArh]'),
#          ('_llpf123',  4132, 0.01,  2, 'U16', 'Power Factor Sum'),
          ('llhz',      4134, 0.1,   1, 'U16', 'Frequency Phase Average [0.1 * Hz]'),
          ('wl1',       4140, 0.01,  0, 'I32', 'Power Real P Phase 1 [0.01 * W]'),
          ('wl2',       4142, 0.01,  0, 'I32', 'Power Real P Phase 2 [0.01 * W]'),
          ('wl3',       4144, 0.01,  0, 'I32', 'Power Real P Phase 3 [0.01 * W]'),
#          ('_ql1',      4146, 0.01,  0, 'I32', 'Power Reactive Q Phase 1 [0.01 * VAr]'),
#          ('_ql2',      4148, 0.01,  0, 'I32', 'Power Reactive Q Phase 2 [0.01 * VAr]'),
#          ('_ql3',      4150, 0.01,  0, 'I32', 'Power Reactive Q Phase 3 [0.01 * VAr]'),
          ('llpf1',     4152, 0.01,  2, 'U16', 'Power Factor Phase 1'),
          ('llpf2',     4153, 0.01,  2, 'U16', 'Power Factor Phase 2'),
          ('llpf3',     4154, 0.01,  2, 'U16', 'Power Factor Phase 3'))

# value_dict = {key: value}
#   key = name in value tuple, index 0
#   value = [decoded_value, decoded_value_string]
value_dict = {}

client = ModbusSerialClient(method = "rtu", port=mb_port, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

#client.connect()

# Read all values with a given address via Modbus
for value in values:
    if value[1] is not None:
        if value[4] == 'U16':
            result = client.read_holding_registers(value[1], 1, unit=mb_id)
        elif value[4] in ('U32', 'I32'):
            result = client.read_holding_registers(value[1], 2, unit=mb_id)
        if result.isError():
            if debug == 1:
                print('Could not read register {} ({})'.format(value[1], value[4]))
            # Default value for not readable values
            decoded_value = 0
            decoded_value_str = '0'
        else:
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            # Check the datatype (default is unsigned int 32 bit)
            if value[4] == 'U16':
                decoded_value_raw = decoder.decode_16bit_uint()
            elif value[4] == 'I32':
                decoded_value_raw = decoder.decode_32bit_int()
            else:
                decoded_value_raw = decoder.decode_32bit_uint()
            # Mulitply the raw value with the corresponding multiplier to get the correct unit
            decoded_value = decoded_value_raw*value[2]
        # Fill the value dictionary with values
        value_dict[value[0]] = [decoded_value, ]

# Generate the value strings for the ramdisk file according to the specified precision
for value in values:
    value_dict[value[0]].append('{:.{prec}f}'.format(value_dict[value[0]][0], prec=value[3]))

# If requried, output all values for debugging
if debug == 1:
    for value in values:
        print('{}: {} ({})'.format(value[0], value_dict[value[0]][1], value[5]))

# Write all values to the ramdisk that are not prefixed with '_'
for value in values:
    if not '_' in value[0]:
        f = open(ramdiskpath + '/' + value[0], 'w')
        f.write(value_dict[value[0]][1])
        f.close()

#client.close()
