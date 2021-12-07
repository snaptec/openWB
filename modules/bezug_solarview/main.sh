#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_solarview/solarview.py "${solarview_hostname}" "${solarview_port}" "${solarview_timeout}" "${debug}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug