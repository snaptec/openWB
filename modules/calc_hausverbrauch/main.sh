#!/bin/bash

sudo python /var/www/html/openWB/modules/calc_hausverbrauch/calc_hausverbrauch.py

hausverbrauch=$(</var/www/html/openWB/ramdisk/hausverbrauch)
echo $hausverbrauch
