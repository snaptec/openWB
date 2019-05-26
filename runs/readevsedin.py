#!/usr/bin/python
from pymodbus.client.sync import ModbusSerialClient
import time

client = ModbusSerialClient(method = "rtu", port="/dev/ttyUSB0", baudrate=9600,
        stopbits=1, bytesize=8, timeout=1)

#client.connect()

rq = client.read_holding_registers(1000,7,unit=1)
print(rq.registers)
time.sleep(0.1)
rq = client.read_holding_registers(2000,10,unit=1)
print(rq.registers)

#client.close()
