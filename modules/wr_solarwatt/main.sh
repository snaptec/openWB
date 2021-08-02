#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
Debug=$debug

python3 /var/www/html/openWB/modules/wr_solarwatt/solarwatt.py $OPENWBBASEDIR $Debug $speicher1_ip
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
