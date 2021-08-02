#!/bin/bash

python3 /var/www/html/openWB/modules/wr_sunways/sunways.py $wrsunwaysip $wrsunwayspw
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt