#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 4024
echo 31 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
