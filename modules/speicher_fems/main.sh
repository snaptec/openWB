#!/bin/bash
soc=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/Soc" | jq .value)
#leistung=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/ActivePower" | jq .value)
grid=$(curl -s "http://x:user@$femsip:8084/rest/channel/_sum/GridActivePower" | jq .value)
pv=$(curl -s "http://x:user@$femsip:8084/rest/channel/_sum/ProductionActivePower" | jq .value)
haus=$(curl -s "http://x:user@$femsip:8084/rest/channel/_sum/ConsumptionActivePower" | jq .value)
speicheriwh=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/ActiveChargeEnergy" | jq .value)
speicherewh=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/ActiveDischargeEnergy" | jq .value)
leistung=$(( grid + pv - haus ))



ra='^[-+]?[0-9]+\.?[0-9]*$'
if ! [[ $soc =~ $ra ]] ; then
	soc="0"
fi
if ! [[ $leistung =~ $ra ]] ; then
		  leistung="0"
fi
echo $soc > /var/www/html/openWB/ramdisk/speichersoc
echo $leistung > /var/www/html/openWB/ramdisk/speicherleistung

echo $speicheriwh > /var/www/html/openWB/ramdisk/speicherikwh
echo $speicherewh > /var/www/html/openWB/ramdisk/speicherekwh

