#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_solarlog/solarlog.py "${bezug_solarlog_ip}" "${bezug_solarlog_speicherv}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
