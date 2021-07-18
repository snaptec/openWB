#!/bin/bash

pv_out=$(curl --connect-timeout 3 -s $pv1_ipa/status )
pv_watt=$(echo $pv_out |jq '.meters[0].power' | sed 's/\..*$//')
# if (( $pv_watt > 0 )); then
# 	pv_watt=$(echo "$pv_watt*-1" |bc)
# fi
pv_watt=$(echo "$pv_watt * -1" | bc)
re='^-?[0-9]+$'
if ! [[ $pv_watt =~ $re ]] ; then
	pv_watt="0"
fi
echo $pv_watt > /var/www/html/openWB/ramdisk/pvwatt
echo $pv_watt
