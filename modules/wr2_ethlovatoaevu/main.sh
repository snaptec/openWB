#!/bin/bash
. /var/www/html/openWB/openwb.conf
	sudo python /var/www/html/openWB/modules/wr2_ethlovatoaevu/readlovato.py 
pvwatt2=$(</var/www/html/openWB/ramdisk/pvwatt2)
echo $pvwatt2


