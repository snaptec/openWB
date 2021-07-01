#!/usr/bin/python
import sys
import os
import time
import getopt
import socket


ipaddress = str(sys.argv[1])

from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=3600)

# Soc
resp= client.read_holding_registers(46, 1,unit=64)
soc = resp.registers[0]
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(soc))
f.close()




##akt. Speicherleistung
resp= client.read_holding_registers(47, 1,unit=64)
sax_pow = resp.registers[0]
# Entladen: negativ
# Laden: positiv
sax_pow *=-1


f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(sax_pow))
f.close()
