#!/usr/bin/python3
import sys

seradd = str(sys.argv[1])
from pymodbus.client.sync import ModbusSerialClient
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
        stopbits=1, bytesize=8, timeout=1)
evseid = int(sys.argv[2])
val = int(sys.argv[3])
rq = client.write_registers(2005, val, unit=evseid)
