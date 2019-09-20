#!/bin/bash
. /var/www/html/openWB/openwb.conf
sudo python /var/www/html/openWB/modules/bezug_alphaess/readalpha.py $alphaessip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug

