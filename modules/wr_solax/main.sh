#!/bin/bash

python3 /var/www/html/openWB/packages/modules/pv/solax.py "${solaxip}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
