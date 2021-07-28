#!/bin/bash

python3 /var/www/html/openWB/modules/bezug_sonneneco/sonneneco.py $sonnenecoalternativ $sonnenecoip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug