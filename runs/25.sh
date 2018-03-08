#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 3245
echo 25 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
