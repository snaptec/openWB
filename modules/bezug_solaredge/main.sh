#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/counter/solaredge.py "${solaredgeip}" "${solaredgemodbusport}" "${solaredgepvslave1}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
