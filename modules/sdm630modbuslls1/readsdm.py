#!/usr/bin/python
import sys
import struct
from pymodbus.client.sync import ModbusSerialClient

serial_port = str(sys.argv[1])
unit_id = int(sys.argv[2])

client = ModbusSerialClient(method="rtu", port=serial_port, baudrate=9600, stopbits=1, bytesize=8, timeout=1)

resp = client.read_input_registers(0x06, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x08, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x0A, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x0C, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x0156, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x0E, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x10, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
# voltages
resp = client.read_input_registers(0x00, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x02, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
resp = client.read_input_registers(0x04, 2, unit=unit_id)
print(struct.unpack('>f', struct.pack('>HH', *resp.registers)))
