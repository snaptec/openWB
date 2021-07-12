#!/bin/bash

python /var/www/html/openWB/modules/wr_victron/victron.py $pv1_ipa
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)

echo $pvwatt
