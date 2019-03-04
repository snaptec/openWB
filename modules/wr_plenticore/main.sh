#!/bin/bash
. /var/www/html/openWB/openwb.conf

		sudo python /var/www/html/openWB/modules/wr_plenticore/plenticore.py $kostalplenticoreip


pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt

