#!/bin/bash

python3 /var/www/html/openWB/packages/modules/pv/victron.py "${pv1_ipa}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
