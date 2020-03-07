#!/usr/bin/python
import sys
import os
import time
import getopt
import socket
import ConfigParser
import struct
import binascii
ipaddress = str(sys.argv[1])
addext = int(sys.argv[2])
from pymodbus.client.sync import ModbusTcpClient
client = ModbusTcpClient(ipaddress, port=502)

#battsoc
resp= client.read_holding_registers(40082,1,unit=1)
value1 = resp.registers[0]
all = format(value1, '04x')
final = int(struct.unpack('>h', all.decode('hex'))[0]) 
f = open('/var/www/html/openWB/ramdisk/speichersoc', 'w')
f.write(str(final))
f.close()
#print "hausverbrauch"
#resp= client.read_holding_registers(40071,2,unit=1)
#value1 = resp.registers[0]
#value2 = resp.registers[1]
#all = format(value2, '04x') + format(value1, '04x')
#final = int(struct.unpack('>i', all.decode('hex'))[0])
#print final
#pv punkt
ext = 0
if addext == 1:
  resp= client.read_holding_registers(40075,2,unit=1)
  value1 = resp.registers[0]
  value2 = resp.registers[1]
  all = format(value2, '04x') + format(value1, '04x')
  ext = int(struct.unpack('>i', all.decode('hex'))[0])
resp= client.read_holding_registers(40067,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0]) * -1
f = open('/var/www/html/openWB/ramdisk/pvwatt', 'w')
f.write(str(final+ext))
f.close()
#battleistung
resp= client.read_holding_registers(40069,2,unit=1)
value1 = resp.registers[0]
value2 = resp.registers[1]
all = format(value2, '04x') + format(value1, '04x')
final = int(struct.unpack('>i', all.decode('hex'))[0])
f = open('/var/www/html/openWB/ramdisk/speicherleistung', 'w')
f.write(str(final))
f.close()
# emulate i e
seconds2= time.time()
watt2= int(final)
watt1=0
seconds1=0.0
if os.path.isfile('/var/www/html/openWB/ramdisk/speichersec0'): 
    f = open('/var/www/html/openWB/ramdisk/speichersec0', 'r')
    seconds1=float(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherwh0', 'r')
    watt1=int(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherwatt0pos', 'r')
    wattposh=int(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherwatt0neg', 'r')
    wattnegh=int(f.read())
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speichersec0', 'w')
    value1 = "%22.6f" % seconds2
    f.write(str(value1))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherwh0', 'w')
    f.write(str(watt2))
    f.close()
    seconds1=seconds1+1
    deltasec = seconds2- seconds1
    deltasectrun =int(deltasec* 1000) / 1000
    stepsize = int((watt2-watt1)/deltasec)
    while seconds1 <= seconds2:
        if watt1 < 0:
            wattnegh= wattnegh + watt1
        else:
            wattposh= wattposh + watt1
        watt1 = watt1 + stepsize
        if stepsize < 0:
            watt1 = max(watt1,watt2)
        else:
            watt1 = min(watt1,watt2)
        seconds1= seconds1 +1
    rest= deltasec - deltasectrun
    seconds1= seconds1  - 1 + rest
    if rest > 0:
        watt1 = int(watt1 * rest)
        if watt1 < 0:
            wattnegh= wattnegh + watt1
        else:
            wattposh= wattposh + watt1
    wattposkh=wattposh/3600
    wattnegkh=(wattnegh*-1)/3600
    f = open('/var/www/html/openWB/ramdisk/speicherwatt0pos', 'w')
    f.write(str(wattposh))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherwatt0neg', 'w')
    f.write(str(wattnegh))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherikwh', 'w')
    f.write(str(wattposkh))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherekwh', 'w')
    f.write(str(wattnegkh))
    f.close()
else: 
    f = open('/var/www/html/openWB/ramdisk/speichersec0', 'w')
    value1 = "%22.6f" % seconds2
    f.write(str(value1))
    f.close()
    f = open('/var/www/html/openWB/ramdisk/speicherwh0', 'w')
    f.write(str(watt2))
    f.close()
  
