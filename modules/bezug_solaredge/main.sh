#!/bin/bash

sudo python /var/www/html/openWB/modules/bezug_solaredge/solaredge.py $solaredgeip $solaredgemodbusport $solaredgepvslave1
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
