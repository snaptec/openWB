#!/bin/bash
sudo python /var/www/html/openWB/runs/dac.py 1427
echo 11 > /var/www/html/openWB/ramdisk/llsoll
echo 1 > /var/www/html/openWB/ramdisk/ladestatus
