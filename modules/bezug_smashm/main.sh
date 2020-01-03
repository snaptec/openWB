#!/bin/bash

. /var/www/html/openWB/openwb.conf

if [ -f "/run/shm/em-"$smashmbezugid"-pconsumecounter" ]; then
	ikwh=$(cat /run/shm/em-$smashmbezugid-pconsumecounter)
	ekwh=$(cat /run/shm/em-$smashmbezugid-psupplycounter)
	bezuga1=$(cat /run/shm/em-$smashmbezugid-p1consume |sed 's/\..*$//')
	bezuga2=$(cat /run/shm/em-$smashmbezugid-p2consume |sed 's/\..*$//')
	bezuga3=$(cat /run/shm/em-$smashmbezugid-p3soncume |sed 's/\..*$//')
	wattbezug=$(cat /run/shm/em-$smashmbezugid-pconsume |sed 's/\..*$//')
	watteinspeisung=$(cat /run/shm/em-$smashmbezugid-pregard |sed 's/\..*$//')
else
	ikwh=$(cat /run/shm/em-$smashmbezugid-pregardcounter)
	ekwh=$(cat /run/shm/em-$smashmbezugid-psurpluscounter)
	bezuga1=$(cat /run/shm/em-$smashmbezugid-p1regard |sed 's/\..*$//')
	bezuga2=$(cat /run/shm/em-$smashmbezugid-p2regard |sed 's/\..*$//')
	bezuga3=$(cat /run/shm/em-$smashmbezugid-p3regard |sed 's/\..*$//')
	wattbezug=$(cat /run/shm/em-$smashmbezugid-pregard |sed 's/\..*$//')
	watteinspeisung=$(cat /run/shm/em-$smashmbezugid-psurplus |sed 's/\..*$//')
fi

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
