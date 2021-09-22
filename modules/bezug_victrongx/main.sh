#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/victron.py "${bezug_victronip}" "${bezug_id}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
