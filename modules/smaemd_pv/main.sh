#!/bin/bash

timeout 3 python3 /var/www/html/openWB/modules/smaemd_pv/sma-em-measurement.py $smaemdpvid
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
