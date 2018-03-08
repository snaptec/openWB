#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 908
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 7 > /var/www/html/openWB/ramdisk/llsoll
