#!/bin/bash

python /var/www/html/openWB/modules/wr_siemens/siemens.py $pv1_ipa
wattbezug=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $wattbezug
