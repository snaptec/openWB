#!/usr/bin/python3
import sys
import os
import time

named_tuple = time.localtime()  # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S ratiotherm off.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
# standard
file_string = bp + str(devicenumber) + '_ratiotherm.log'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
if os.path.isfile(file_string):
    pass
else:
    with open(file_string, 'w') as f:
        print('ratiotherm start log', file=f)
with open(file_string, 'a') as f:
    print('%s devicenr %s ipadr %s ueberschuss %6d try to connect (modbus)'
          % (time_string, devicenumber, ipadr, uberschuss), file=f)
aktpower = 0
with open(file_string, 'a') as f:
    print('%s devicenr %s ipadr %s Akt Leistung  %6d'
          % (time_string, devicenumber, ipadr, aktpower), file=f)
pvmodus = 0
if os.path.isfile(file_stringpv):
    with open(file_stringpv, 'r') as f:
        pvmodus = int(f.read())
# wenn vorher pvmodus an, dann watt.py
# signaliseren einmalig 0 ueberschuss zu schicken
if pvmodus == 1:
    pvmodus = 99
with open(file_stringpv, 'w') as f:
    f.write(str(pvmodus))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
