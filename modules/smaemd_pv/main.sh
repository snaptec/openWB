#!/bin/bash

. /var/www/html/openWB/openwb.conf


ipvwh=$(cat /run/shm/em-$smaemdpvid-psurpluscounter)
pvwatt=$(cat /run/shm/em-$smaemdpvid-psurplus |sed 's/\..*$//')
ipvwh=$(echo "($ipvwh*1000)" |bc)
echo $ipvwh > /var/www/html/openWB/ramdisk/pvkwh
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt

