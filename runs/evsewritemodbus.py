#!/usr/bin/python3
import sys

seradd = str(sys.argv[1])
from pymodbus.client.sync import ModbusSerialClient
client = ModbusSerialClient(method = "rtu", port=seradd, baudrate=9600,
        stopbits=1, bytesize=8, timeout=1)
evseid = int(sys.argv[2])
lla = int(sys.argv[3])
rq = client.write_registers(1000, lla, unit=evseid)
