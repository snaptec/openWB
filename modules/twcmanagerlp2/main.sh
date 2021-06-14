#!/bin/bash
re='^[-+]?[0-9]+\.?[0-9]*$'

# debugging @todo remove after testing!
. /var/www/html/openWB/openwb.conf

if [ $twcmanagerlp2httpcontrol -eq 1 ]; then
	twcmanagerlp2phasen=$(curl --connect-timeout 3 -s "http://$twcmanagerlp2ip:$twcmanagerlp2port/api/getConfig" | jq .config.numberOfPhases)
	status=$(curl --connect-timeout 3 -s "http://$twcmanagerlp2ip:$twcmanagerlp2port/api/getStatus")
	amps=$(echo $status | jq .consumptionAmps | sed -e 's/^"//' -e 's/"$//')
	watts=$(echo $status | jq .consumptionWatts | sed -e 's/^"//' -e 's/"$//')
	watt=$(echo "scale=0;$watts / $twcmanagerlp2phasen" | bc | sed 's/\..*$//')
else
	amps=$(curl --connect-timeout 3 -s "http://$twcmanagerlp2ip/index.php" |grep Charging | sed 's/^.*\(Charging at.*A\).*$/\1/' | cut -c 13- | tr -d A)
	watt=$(echo "scale=0;$amps * 230  * $twcmanagerlp2phasen" | bc | sed 's/\..*$//')
fi

# @todo amps without " / parse to int
echo "###########################################"
echo "# DEBUG ###################################"
echo "###########################################"
echo "Phases:           $twcmanagerlp2phasen"
echo "Current Amps:     $amps"
echo "Current Watts:    $watts"
echo "Watt per Phase:   $watt"
echo "###########################################"
exit

if ! [[ $amps =~ $re ]] ; then
	amps="0"
fi
if (( twcmanagerlp2phasen == 1 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
fi
if (( twcmanagerlp2phasen == 2 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
fi
if (( twcmanagerlp2phasen == 3 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
	echo $amps > /var/www/html/openWB/ramdisk/llas13
fi

echo $watt > /var/www/html/openWB/ramdisk/llaktuells1
