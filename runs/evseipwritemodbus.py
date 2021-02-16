#!/usr/bin/python3
import sys
from pymodbus.client.sync import ModbusTcpClient

lla = int(sys.argv[1])
ipadd = str(sys.argv[2])
evseid = int(sys.argv[3])

client = ModbusTcpClient(ipadd, port=8899)
rq = client.write_registers(1000, lla, unit=evseid)
