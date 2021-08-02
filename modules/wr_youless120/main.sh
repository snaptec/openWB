#!/bin/bash

python3 /var/www/html/openWB/modules/wr_youless120/youless.py $wryoulessip $wryoulessalt
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt) 
echo $pvwatt
