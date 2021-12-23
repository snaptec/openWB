#!/bin/bash

sudo python /var/www/html/openWB/modules/wr2_smamodbus/sma.py $pv2ip

pv2watt=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pv2watt
