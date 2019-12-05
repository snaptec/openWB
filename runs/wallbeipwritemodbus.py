#!/usr/bin/python3
import sys
from pymodbus.client.sync import ModbusTcpClient

lla = int(sys.argv[1])
ipadd = "192.168.0.8" # wallbe default
if len(sys.argv) > 1:
    ipadd = str(sys.argv[2])
devid = 255 # wallbe default
if len(sys.argv) > 2:
    devid = int(sys.argv[2])

client = ModbusTcpClient(ipadd, port=502)
rq = client.write_registers(528, lla, unit=devid)
