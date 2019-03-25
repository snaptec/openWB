#!/bin/bash
. /var/www/html/openWB/openwb.conf

if (( kostalplenticorebatt == 1 )); then
	sudo python /var/www/html/openWB/modules/wr_plenticore/plenticorebatt.py $kostalplenticoreip
else
	sudo python /var/www/html/openWB/modules/wr_plenticore/plenticore.py $kostalplenticoreip
fi

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt

