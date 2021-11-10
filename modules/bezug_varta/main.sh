#!/bin/bash

python /var/www/html/openWB/modules/bezug_varta/varta.py $vartaspeicherip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
