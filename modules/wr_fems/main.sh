#!/bin/bash
. /var/www/html/openWB/openwb.conf

pvwatt=$(curl -s "http://x:user@$femsip:8084/rest/channel/charger0/ActualPower" | jq .value)
pvwatt=$(( pvwatt * -1 ))
pvwh=$(curl -s "http://x:user@$femsip:8084/rest/channel/charger0/ActualEnergy" | jq .value)

re='^-?[0-9]+$'
if ! [[ $pvwatt =~ $re ]] ; then
   pvwatt="0"
fi
if [[ $pvwh =~ $re ]] ; then
		echo $pvwh > /var/www/html/openWB/ramdisk/pvkwh
fi
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvwatt
