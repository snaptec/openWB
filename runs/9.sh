#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 1168
echo 9 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
