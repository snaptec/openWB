#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_kostalpiko/kostal_piko.py "${wrkostalpikoip}" "${speichermodul}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug