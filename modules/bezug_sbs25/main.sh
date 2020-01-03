#!/bin/bash
. /var/www/html/openWB/openwb.conf



sudo python /var/www/html/openWB/modules/bezug_sbs25/sbs25.py $sbs25ip

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug




