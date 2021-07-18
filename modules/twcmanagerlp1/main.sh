#!/bin/bash
re='^[-+]?[0-9]+\.?[0-9]*$'

if [[ $twcmanagerlp1httpcontrol -eq 1 ]]; then
	status=$(curl --connect-timeout 3 -s "http://$twcmanagerlp1ip:$twcmanagerlp1port/api/getStatus")
	amps=$(echo $status | jq .maxAmpsToDivideAmongSlaves | sed -e 's/^"//' -e 's/"$//')
	watts=$(echo $status | jq .chargerLoadWatts | sed -e 's/^"//' -e 's/"$//')
	watt=$(echo "scale=0;$watts" | bc | sed 's/\..*$//')

	if [[ $watt -lt 4000 ]]; then
		twcmanagerlp1phasen=1
	elif [[ $watt -lt 8000 ]]; then
		twcmanagerlp1phasen=2
	else
		twcmanagerlp1phasen=3
	fi
else
	amps=$(curl --connect-timeout 3 -s "http://$twcmanagerlp1ip/index.php" | grep Charging | sed 's/^.*\(Charging at.*A\).*$/\1/' | cut -c 13- | tr -d A)
	watt=$(echo "scale=0;$amps * 230  * $twcmanagerlp1phasen" | bc | sed 's/\..*$//')
fi

if ! [[ $amps =~ $re ]] ; then
	amps="0"
fi

if (( twcmanagerlp1phasen == 1 )); then
	echo $amps > /var/www/html/openWB/ramdisk/lla1
        echo 0 > /var/www/html/openWB/ramdisk/lla2
        echo 0 > /var/www/html/openWB/ramdisk/lla3
elif (( twcmanagerlp1phasen == 2 )); then
	echo $amps > /var/www/html/openWB/ramdisk/lla1
	echo $amps > /var/www/html/openWB/ramdisk/lla2
	echo 0 > /var/www/html/openWB/ramdisk/lla3
elif (( twcmanagerlp1phasen == 3 )); then
	echo $amps > /var/www/html/openWB/ramdisk/lla1
	echo $amps > /var/www/html/openWB/ramdisk/lla2
	echo $amps > /var/www/html/openWB/ramdisk/lla3
fi

echo $watt > /var/www/html/openWB/ramdisk/llaktuell



