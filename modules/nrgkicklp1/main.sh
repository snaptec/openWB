#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

##set charging
##curl -s -X PUT -H "Content-Type: application/json" --data '{ "Values": {"ChargingStatus": { "Charging": false }, "ChargingCurrent": { "Value": "6"}, "DeviceMetadata":{"Password": 1234}}}' 10.20.0.78/api/settings/00:1E:C0:76:82:1D

output=$(curl --connect-timeout $nrgkicktimeoutlp1 -s http://$nrgkickiplp1/api/measurements/$nrgkickmaclp1)
if [[ $? == "0" ]] ; then
	watt=$(echo $output | jq -r '.ChargingPower')
	watt=$(echo "scale=0;$watt * 1000 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		echo $watt > /var/www/html/openWB/ramdisk/llaktuell
	fi
	lla1=$(echo $output | jq -r '.ChargingCurrentPhase[0]')
	lla1=$(echo "scale=0;$lla1 / 1" |bc)
	if [[ $lla1 =~ $re ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/lla1
	fi
	lla2=$(echo $output | jq -r '.ChargingCurrentPhase[1]')
	lla2=$(echo "scale=0;$lla2 / 1" |bc)
	if [[ $lla2 =~ $re ]] ; then
		echo $lla2 > /var/www/html/openWB/ramdisk/lla2
	fi
	lla3=$(echo $output | jq -r '.ChargingCurrentPhase[2]')
	lla3=$(echo "scale=0;$lla3 / 1" |bc)
	if [[ $lla3 =~ $re ]] ; then
		echo $lla3 > /var/www/html/openWB/ramdisk/lla3
	fi
	llv1=$(echo $output | jq -r '.VoltagePhase[0]')
	if [[ $lla1 =~ $re ]] ; then
		echo $llv1 > /var/www/html/openWB/ramdisk/llv1
	fi
	llv2=$(echo $output | jq -r '.VoltagePhase[1]')
	if [[ $lla2 =~ $re ]] ; then
		echo $llv2 > /var/www/html/openWB/ramdisk/llv2
	fi
	llv3=$(echo $output | jq -r '.VoltagePhase[2]')
	if [[ $lla3 =~ $re ]] ; then
		echo $llv3 > /var/www/html/openWB/ramdisk/llv3
	fi
	llkwh=$(echo $output | jq -r '.ChargingEnergyOverAll')
	llkwh=$(echo "scale=3;$llkwh / 1" |bc)
	if [[ $llkwh =~ $rekwh ]] ; then
		echo $llkwh > /var/www/html/openWB/ramdisk/llkwh
	fi
fi
