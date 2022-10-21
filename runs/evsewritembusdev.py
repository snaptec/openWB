#!/usr/bin/python3
import sys
from pymodbus.client.sync import ModbusSerialClient

seradd = str(sys.argv[1])
evseid = int(sys.argv[2])
wreg = int(sys.argv[3])
val = int(sys.argv[4])

client = ModbusSerialClient(method="rtu", port=seradd, baudrate=9600, stopbits=1, bytesize=8, timeout=1)
rq = client.write_registers(wreg, val, unit=evseid)
