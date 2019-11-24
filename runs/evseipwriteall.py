#!/usr/bin/python3
import sys
ipadd = str(sys.argv[2])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipadd, port=8899)
lla = int(sys.argv[1])
evseid = int(sys.argv[3])
wreg = int(sys.argv[4])
rq = client.write_registers(wreg, lla, unit=evseid)
