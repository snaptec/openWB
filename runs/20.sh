#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 2596
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 20 > /var/www/html/openWB/ramdisk/llsoll
