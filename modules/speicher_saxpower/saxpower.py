#!/usr/bin/python
import sys
# import os
# import time
# import getopt
# import socket
from pymodbus.client.sync import ModbusTcpClient

ipaddress = str(sys.argv[1])

client = ModbusTcpClient(ipaddress, port=3600)

# Register auslesen
resp= client.read_holding_registers(46, 2,unit=64)

# SOC
soc = resp.registers[0]
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(soc))
f.close()

# akt. Speicherleistung
sax_pow=resp.registers[1]
# unsigned to signed int
if sax_pow > 32767:
    sax_pow -= 65535

# Entladen: negativ
# Laden: positiv
sax_pow *=-1

f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(sax_pow))
f.close()
