#!/bin/bash
python /var/www/html/openWB/modules/wr2_sungrow/sungrow.py $pv2ip
pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pvwatt
