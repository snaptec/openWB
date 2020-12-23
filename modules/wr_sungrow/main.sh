#!/bin/bash
python /var/www/html/openWB/modules/wr_sungrow/sungrow.py $speicher1_ip
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
