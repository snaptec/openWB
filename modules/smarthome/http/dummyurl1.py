#!/usr/bin/python3
import sys
import os
import time
numbers=sys.argv[1]
number=int(numbers)
basePath = '/var/www/html/openWB'
try:
    f = open(basePath+'/ramdisk/device' + str(number) + '_req_relais', 'r')
    status =int(f.read())
    f.close()
except Exception as e:
    status = 0
status = status * 100
print(status)
