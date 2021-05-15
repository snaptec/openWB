#!/bin/bash

pvwatt=$(curl -s "http://x:$femskacopw@$femsip:8084/rest/channel/_sum/ProductionActivePower" | jq .value)
pvwatt=$(( pvwatt * -1 ))
pvwh=$(curl -s "http://x:$femskacopw@$femsip:8084/rest/channel/_sum/ProductionActiveEnergy" | jq .value)

re='^-?[0-9]+$'
if ! [[ $pvwatt =~ $re ]] ; then
   pvwatt="0"
fi
if [[ $pvwh =~ $re ]] ; then
		echo $pvwh > /var/www/html/openWB/ramdisk/pvkwh
fi
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvwatt
