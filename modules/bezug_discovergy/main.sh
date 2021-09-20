#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/discovergy.py "${discovergyuser}" "${discovergypass}" "${discovergyevuid}"
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug