#!/bin/bash
re='^[-+]?[0-9]+\.?[0-9]*$'
amps=$(curl --connect-timeout 3 -s "http://$twcmanagerlp1ip/index.php" |grep Charging | sed 's/^.*\(Charging at.*A\).*$/\1/' | cut -c 13- | tr -d A)

if ! [[ $amps =~ $re ]] ; then
	amps="0"
fi
if (( twcmanagerlp1phasen == 1 )); then
	watt=$(echo "scale=0;$amps * 230 /1" | bc | sed 's/\..*$//')
	echo $amps > /var/www/html/openWB/ramdisk/lla1
fi
if (( twcmanagerlp1phasen == 2 )); then
	watt=$(echo "scale=0;$amps * 230 * 2" | bc | sed 's/\..*$//')
	echo $amps > /var/www/html/openWB/ramdisk/lla1
	echo $amps > /var/www/html/openWB/ramdisk/lla2
fi
if (( twcmanagerlp1phasen == 3 )); then
	watt=$(echo "scale=0;$amps * 230 * 3" | bc | sed 's/\..*$//')
	echo $amps > /var/www/html/openWB/ramdisk/lla1
	echo $amps > /var/www/html/openWB/ramdisk/lla2
	echo $amps > /var/www/html/openWB/ramdisk/lla3

fi
echo $watt > /var/www/html/openWB/ramdisk/llaktuell



