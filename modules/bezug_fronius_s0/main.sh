#!/bin/bash

sudo python3 /var/www/html/openWB/modules/bezug_fronius_s0/fronius_s0.py $froniusprimo $wrfroniusip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
