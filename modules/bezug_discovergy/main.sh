#!/bin/bash

sudo python3 /var/www/html/openWB/modules/bezug_discovergy/discovergy.py $discovergyuser $discovergypass $discovergyevuid
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug