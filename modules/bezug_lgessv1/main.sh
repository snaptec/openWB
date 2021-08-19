#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_lgessv1/lgessv1.py "${lgessv1ip}" "${lgessv1pass}" "${ess_api_ver}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
