#!/bin/bash
# debug start
twcngardinerlp2ip=127.0.0.1
twcngardinerlp2port=8080
# debug end

re='^[-+]?[0-9]+\.?[0-9]*$'
phases=$(curl --connect-timeout 3 -s "http://$twcngardinerlp2ip:$twcngardinerlp2port/api/getConfig" | jq .config.numberOfPhases)
status=$(curl --connect-timeout 3 -s "http://$twcngardinerlp2ip:$twcngardinerlp2port/api/getStatus")
amps=$(echo $status | jq .consumptionAmps | sed -e 's/^"//' -e 's/"$//')
watts=$(echo $status | jq .consumptionWatts | sed -e 's/^"//' -e 's/"$//')
watt=$(echo "scale=0;$watts / $phases" | bc | sed 's/\..*$//')

# @todo get watts & amps from getStatus
# @todo aps without " / parse to int
echo "Phases:		$phases"
echo "Current Amps:	$amps"
echo "Current Watts:	$watts"
echo "Watt per Phase:	$watt"
exit

if ! [[ $amps =~ $re ]] ; then
	amps="0"
fi
if (( phases == 1 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
fi
if (( phases == 2 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
fi
if (( phases == 3 )); then
	echo $amps > /var/www/html/openWB/ramdisk/llas11
	echo $amps > /var/www/html/openWB/ramdisk/llas12
	echo $amps > /var/www/html/openWB/ramdisk/llas13
fi

echo $watt > /var/www/html/openWB/ramdisk/llaktuells1



