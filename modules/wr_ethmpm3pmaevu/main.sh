#!/bin/bash

python3 /var/www/html/openWB/packages/modules/pv/openwb.py "${pvkitversion}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
