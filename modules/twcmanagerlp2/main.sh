#!/bin/bash
re='^[-+]?[0-9]+\.?[0-9]*$'

if [[ $twcmanagerlp2httpcontrol -eq 1 ]]; then
	slave=$(curl --connect-timeout 3 -s "http://$twcmanagerlp2ip:$twcmanagerlp2port/api/getSlaveTWCs")
	status=$(curl --connect-timeout 3 -s "http://$twcmanagerlp2ip:$twcmanagerlp2port/api/getStatus")
	amps=$(echo "$slave" | jq 'first(.[].reportedAmpsActual)' | sed -e 's/^"//' -e 's/"$//')
	watts=$(echo "$status" | jq .chargerLoadWatts | sed -e 's/^"//' -e 's/"$//')
	watt=$(echo "scale=0;$watts" | bc | sed 's/\..*$//')

	volt1=$(echo "$slave" | jq 'first(.[].voltsPhaseA)')
	volt2=$(echo "$slave" | jq 'first(.[].voltsPhaseB)')
	volt3=$(echo "$slave" | jq 'first(.[].voltsPhaseC)')
	kwh_total=$(echo "$slave" | jq '.total.lifetimekWh')

	echo $volt1 > /var/www/html/openWB/ramdisk/llvs11
	echo $volt2 > /var/www/html/openWB/ramdisk/llvs12
	echo $volt3 > /var/www/html/openWB/ramdisk/llvs13
	echo $kwh_total > /var/www/html/openWB/ramdisk/llkwhs1

	if [[ $watt -lt 4000 ]]; then
		twcmanagerlp2phasen=1
	elif [[ $watt -lt 8000 ]]; then
		twcmanagerlp2phasen=2
	else
		twcmanagerlp2phasen=3
	fi
else
	amps=$(curl --connect-timeout 3 -s "http://$twcmanagerlp2ip/index.php" | grep Charging | sed 's/^.*\(Charging at.*A\).*$/\1/' | cut -c 13- | tr -d A)
	watt=$(echo "scale=0;$amps * 230  * $twcmanagerlp2phasen" | bc | sed 's/\..*$//')
fi

if ! [[ $amps =~ $re ]] ; then
	amps="0"
fi

if (( twcmanagerlp2phasen == 1 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo 0 > /var/www/html/openWB/ramdisk/llas12
	echo 0 > /var/www/html/openWB/ramdisk/llas13
elif (( twcmanagerlp2phasen == 2 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
	echo 0 > /var/www/html/openWB/ramdisk/llas13
elif (( twcmanagerlp2phasen == 3 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
	echo $amps > /var/www/html/openWB/ramdisk/llas13
fi

echo $watt > /var/www/html/openWB/ramdisk/llaktuells1
