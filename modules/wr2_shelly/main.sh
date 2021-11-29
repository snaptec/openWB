#!/bin/bash

sudo python3 /var/www/html/openWB/modules/wr2_shelly/shellywr.py $pv2ip pv2watt 
pvwatt2=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pvwatt2
