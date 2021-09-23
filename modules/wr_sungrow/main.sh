#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/pv/sungrow.py "${speicher1_ip}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
