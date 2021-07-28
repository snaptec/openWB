#!/bin/bash

python /var/www/html/openWB/modules/bezug_kostalplenticoreem300haus/kostal_plenticore.py $kostalplenticorehaus
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
