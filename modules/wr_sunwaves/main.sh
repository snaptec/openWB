#!/bin/bash

python3 /var/www/html/openWB/modules/wr_sunwaves/sunwaves.py $wrsunwavesip $wrsunwavespw
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
