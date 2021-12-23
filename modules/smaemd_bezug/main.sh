#!/bin/bash

ikwh=$(cat /run/shm/em-$smaemdbezugid-pregardcounter)
ekwh=$(cat /run/shm/em-$smaemdbezugid-psurpluscounter)
bezuga1=$(cat /run/shm/em-$smaemdbezugid-p1regard |sed 's/\..*$//')
bezuga2=$(cat /run/shm/em-$smaemdbezugid-p2regard |sed 's/\..*$//')
bezuga3=$(cat /run/shm/em-$smaemdbezugid-p3regard |sed 's/\..*$//')
wattbezug=$(cat /run/shm/em-$smaemdbezugid-pregard |sed 's/\..*$//')
watteinspeisung=$(cat /run/shm/em-$smaemdbezugid-psurplus |sed 's/\..*$//')

ikwh=$(echo "($ikwh*1000)" |bc)
ekwh=$(echo "($ekwh*1000)" |bc)
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
bezuga1=$(echo "scale=3;$bezuga1/230" | bc -l)
bezuga2=$(echo "scale=3;$bezuga2/230" | bc -l)
bezuga3=$(echo "scale=3;$bezuga3/230" | bc -l)
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3

if (( $watteinspeisung > 5 ));then
	wattbezug=$(echo -$watteinspeisung)
fi
echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
