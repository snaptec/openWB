#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 0
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo "setz ladung auf 0A" >> /var/www/html/openWB/web/lade.log
echo 0 > /var/www/html/openWB/ramdisk/llsoll
