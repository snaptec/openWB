#!/usr/bin/python3
import sys
# import os
import time
# import getopt
import socket

named_tuple = time.localtime() # getstruct_time
time_string = time.strftime("%m/%d/%Y, %H:%M:%S check502.py", named_tuple)

ipaddress = str(sys.argv[1])
file_string= '/var/www/html/openWB/ramdisk/port_502_' + ipaddress

try:
    f = open( file_string , 'r')
    port =int(f.read())
    f.close()
except:
    port = 9

if (port == 1) or (port == 0):
    pass
else:
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (ipaddress, 502)
    result_of_check = a_socket.connect_ex(location)
    f = open( file_string , 'w')
    if result_of_check == 0:
        f.write(str(1))
        print ('%s ipadr %s Port 502 is open ' % (time_string,ipaddress))
        #print(ipaddress," Port 502 is open")
    else:
        f.write(str(0))
        print ('%s ipadr %s Port 502 is not open ' % (time_string,ipaddress))
        #print(ipaddress," Port 502 is not open")
    a_socket.close()
    f.close()
