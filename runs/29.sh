#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 3764
echo 29 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
