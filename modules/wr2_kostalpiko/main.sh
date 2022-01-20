#!/bin/bash

python3 /var/www/html/openWB/modules/wr_kostalpiko/kostal_piko_var1.py 2 $speichermodul $pv2ip
pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt) 
echo $pvwatt
