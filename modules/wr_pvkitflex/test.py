#!/usr/bin/python
import sys
# import os
# import time
# import getopt
import struct
from pymodbus.client.sync import ModbusTcpClient

##PV Kit Defaults
mbip='192.168.193.13'
mbport=8899
mbid = 115
numpv=1

#Check Argumentlist and replace Defaults if present
if len(sys.argv) >= 2:
        numpv=int(sys.argv[1])

if len(sys.argv) >= 3:
        mbip=str(sys.argv[2])

if len(sys.argv) >= 4:
        mbport=int(sys.argv[3])

if len(sys.argv) >= 5:
        mbid=int(sys.argv[4])


print('Anzahl: ' + str(len(sys.argv)) + ' MBIP: ' + mbip + ' MBPort: ' + str(mbport) + ' SDMID: ' +str(mbid)+ ' NUMPV: ' + str(numpv))


if numpv == 1:
	with open('/var/www/html/openWB/ramdisk/pvwatt', 'w') as f:
		f.write(str(mbport))
else:
	with open('/var/www/html/openWB/ramdisk/pv' + str(numpv)+ 'watt', 'w') as f:
		f.write(str(mbport))

#exit(1)
exit(0)
