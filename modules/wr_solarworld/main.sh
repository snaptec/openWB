#!/bin/bash

python3 /var/www/html/openWB/modules/wr_solarworld/solarworld.py $solarworld_emanagerip
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
