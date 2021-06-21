#!/usr/bin/python
import sys
import os
import time
from pymodbus.client.sync import ModbusTcpClient

seradd = str(sys.argv[1])
serid = int(4)

client = ModbusTcpClient(seradd, port=8899)
rq = client.write_register(0x0001, 256, unit=serid)
time.sleep(2)
rq = client.write_register(0x0001, 512, unit=serid)
