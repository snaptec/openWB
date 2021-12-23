#!/bin/bash

sudo python3 /var/www/html/openWB/modules/wr_shelly/shellywr.py $pv1_ipa pvwatt
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt