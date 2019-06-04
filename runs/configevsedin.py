#!/usr/bin/python
from pymodbus.client.sync import ModbusSerialClient
import time

# Set the maximum allowed current:
default_amps_value = 20

client = ModbusSerialClient(method = "rtu", port="/dev/ttyUSB0", baudrate=9600,
        stopbits=1, bytesize=8, timeout=1)

#client.connect()

print('First read the registers 2000 to 2009...')
rr = client.read_holding_registers(2000, 10, unit=1)
print(rr.registers)

time.sleep(0.1)
print('Then set the maximum allowed current to {}A.'.format(default_amps_value))
# Attention: The function "client.write_register" (for a single register) is NOT implemented!
rq = client.write_registers(2000, default_amps_value, unit=1)
if rq.isError():
    print('ERROR: Writing to the "Default amps value" register 2000 failed')

time.sleep(0.1)
print('Now read the registers 2000 to 2009 a second time for verification...')
rr = client.read_holding_registers(2000, 10, unit=1)
print(rr.registers)

#client.close()
