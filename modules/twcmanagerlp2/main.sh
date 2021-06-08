#!/bin/bash
re='^[-+]?[0-9]+\.?[0-9]*$'
amps=$(curl --connect-timeout 3 -s "http://$twcmanagerlp2ip/index.php" |grep Charging | sed 's/^.*\(Charging at.*A\).*$/\1/' | cut -c 13- | tr -d A)

if ! [[ $amps =~ $re ]] ; then
	amps="0"
fi
if (( twcmanagerlp2phasen == 1 )); then
	watt=$(echo "scale=0;$amps * 230 /1" | bc | sed 's/\..*$//')
	echo $amps > /var/www/html/openWB/ramdisk/llas11
fi
if (( twcmanagerlp2phasen == 2 )); then
	watt=$(echo "scale=0;$amps * 230 * 2" | bc | sed 's/\..*$//')
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
fi
if (( twcmanagerlp2phasen == 3 )); then
	watt=$(echo "scale=0;$amps * 230 * 3" | bc | sed 's/\..*$//')
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
	echo $amps > /var/www/html/openWB/ramdisk/llas13
fi

echo $watt > /var/www/html/openWB/ramdisk/llaktuells1



