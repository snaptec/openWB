#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/pv/pv_kit.py "${pvkitversion}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
