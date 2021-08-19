#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_smartme/smartme.py "${bezug_smartme_url}" "${bezug_smartme_user}" "${bezug_smartme_pass}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug