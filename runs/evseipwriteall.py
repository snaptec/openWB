#!/usr/bin/python3
import sys
from pymodbus.client.sync import ModbusTcpClient

lla = int(sys.argv[1])
ipadd = str(sys.argv[2])
evseid = int(sys.argv[3])
wreg = int(sys.argv[4])

client = ModbusTcpClient(ipadd, port=8899)
rq = client.write_registers(wreg, lla, unit=evseid)
