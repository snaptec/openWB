#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 3634
echo 28 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
