#!/bin/bash
. /var/www/html/openWB/openwb.conf



sudo python /var/www/html/openWB/modules/wr_solaredge/solaredge.py $pvsolaredgeip
wattbezug=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
