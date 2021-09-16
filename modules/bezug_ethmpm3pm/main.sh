#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/openwb.py "${evukitversion}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
