#!/bin/bash
. /var/www/html/openWB/openwb.conf

sudo python /var/www/html/openWB/modules/wr_ethmpm3pmaevu/readmpm3pm.py 
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt


