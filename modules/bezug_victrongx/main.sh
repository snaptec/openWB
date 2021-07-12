#!/bin/bash

sudo python /var/www/html/openWB/modules/bezug_victrongx/victron.py $bezug_victronip $bezug_id

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
