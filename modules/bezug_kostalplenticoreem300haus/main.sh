#!/bin/bash
. /var/www/html/openWB/openwb.conf

		sudo python /var/www/html/openWB/modules/bezug_kostalplenticoreem300haus/plenticore.py $kostalplenticoreip $kostalplenticorehaus


bezugwatt=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $bezugwatt

