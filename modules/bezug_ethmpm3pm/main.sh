#!/bin/bash
. /var/www/html/openWB/openwb.conf

sudo python /var/www/html/openWB/modules/bezug_ethmpm3pm/readmpm3pm.py 
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug


