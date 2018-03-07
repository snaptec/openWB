#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 790
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
echo 6 > /var/www/html/openWB/ramdisk/llsoll
