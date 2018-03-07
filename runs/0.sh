#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 0
echo 0 > /var/www/html/openWB/ramdisk/ladestatus
echo 0 > /var/www/html/openWB/ramdisk/llsoll
