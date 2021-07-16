#!/bin/bash
input=$(echo $1)
temp="${input#*d=}"
d=${temp:0:1}
sudo python3 /var/www/html/openWB/modules/smarthome/http/dummyurl1.py $d 
#sudo python3 /var/www/html/openWB/modules/smarthome/http/dummyurl1.py $d >> /var/www/html/openWB/ramdisk/xxlog.log 2>&1
