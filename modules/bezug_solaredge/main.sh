#!/bin/bash
. /var/www/html/openWB/openwb.conf



sudo python /var/www/html/openWB/modules/bezug_solaredge/solaredge.py $solaredgeip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
