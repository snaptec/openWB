#!/bin/bash

python /var/www/html/openWB/modules/wr_solax/solax.py $solaxip

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
