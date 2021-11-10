#!/bin/bash

illwh=$(cat /run/shm/em-$smaemdllid-pregardcounter)
llwatt=$(cat /run/shm/em-$smaemdllid-pregard |sed 's/\..*$//')
bezuga1=$(cat /run/shm/em-$smaemdllid-p1regard |sed 's/\..*$//')
bezuga2=$(cat /run/shm/em-$smaemdllid-p2regard |sed 's/\..*$//')
bezuga3=$(cat /run/shm/em-$smaemdllid-p3regard |sed 's/\..*$//')

echo $illwh > /var/www/html/openWB/ramdisk/llkwh
echo $llwatt > /var/www/html/openWB/ramdisk/llaktuell
echo $bezuga1 > /var/www/html/openWB/ramdisk/lla1
echo $bezuga2 > /var/www/html/openWB/ramdisk/lla2
echo $bezuga3 > /var/www/html/openWB/ramdisk/lla3
