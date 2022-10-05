#!/usr/bin/python3
import sys
import os
import time
named_tuple = time.localtime()   # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S N4DAC02 on.py", named_tuple)
devicenumber = str(sys.argv[1])
ipadr = str(sys.argv[2])
uberschuss = int(sys.argv[3])
bp = '/var/www/html/openWB/ramdisk/smarthome_device_'
file_string = bp + str(devicenumber) + '_N4DAC02.log'
file_stringpv = bp + str(devicenumber) + '_pv'
file_stringcount = bp + str(devicenumber) + '_count'
file_stringcount5 = bp + str(devicenumber) + '_count5'
if os.path.isfile(file_string):
    pass
else:
    with open(file_string, 'w') as f:
        print('N4DAC02 start log', file=f)
with open(file_string, 'a') as f:
    print('%s devicenr %s ipadr %s' %
          (time_string, devicenumber, ipadr), file=f)
pvmodus = 1
with open(file_stringpv, 'w') as f:
    f.write(str(pvmodus))
count1 = 999
with open(file_stringcount, 'w') as f:
    f.write(str(count1))
count5 = 999
with open(file_stringcount5, 'w') as f:
    f.write(str(count5))
