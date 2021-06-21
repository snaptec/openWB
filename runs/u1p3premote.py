#!/usr/bin/python
from pymodbus.client.sync import ModbusTcpClient
import sys
import os
import time
seradd = str(sys.argv[1])
serid = int(sys.argv[2])

from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(seradd, port=8899)
if ( str(sys.argv[3]) == "1" ):
    rq = client.write_register(0x0001, 256, unit=serid)
    time.sleep(1)
    rq = client.write_register(0x0001, 512, unit=serid)

if ( str(sys.argv[3]) == "3" ):
    rq = client.write_register(0x0002, 256, unit=serid)
    time.sleep(1)
    rq = client.write_register(0x0002, 512, unit=serid)

