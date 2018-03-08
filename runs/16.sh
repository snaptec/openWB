#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 2077
echo 16 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
