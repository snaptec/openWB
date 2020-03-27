#!/bin/bash
. /var/www/html/openWB/openwb.conf
soc=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/Soc" | jq .value)
leistung=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/ActivePower" | jq .value)
leistung=$(( leistung * -1 ))
speicheriwh=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/ActiveChargeEnergy" | jq .value)
speicherewh=$(curl -s "http://x:user@$femsip:8084/rest/channel/ess0/ActiveDischargeEnergy" | jq .value)


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

