#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/pv/sdm120.py "${wr_sdm120ip}" "${wr_sdm120id}" 

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
