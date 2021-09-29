#!/bin/bash

python3 /var/www/html/openWB/packages/modules/pv/siemens.py "${pv1_ipa}"

wattbezug=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $wattbezug
