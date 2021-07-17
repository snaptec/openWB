#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

output=$(curl --connect-timeout $evsewifitimeoutlp3 -s http://$evsewifiiplp3/getParameters)
if ! [ -z "$output" ]; then
	watt=$(echo $output | jq '.list[] | .actualPower')
	lla1=$(echo $output | jq '.list[] | .currentP1')
	lla2=$(echo $output | jq '.list[] | .currentP2')
	lla3=$(echo $output | jq '.list[] | .currentP3')
	llv1=$(echo $output | jq '.list[] | .voltageP1')
	llv2=$(echo $output | jq '.list[] | .voltageP2')
	llv3=$(echo $output | jq '.list[] | .voltageP3')
	llkwh=$(echo $output | jq '.list[] | .meterReading')
	evsewifiplugstatelp3=$(echo $output | jq '.list[] | .vehicleState') 

	watt=$(echo "scale=0;$watt * 1000 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		echo $watt > /var/www/html/openWB/ramdisk/llaktuells2
	fi
	if [[ $lla1 =~ $re ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/llas21
	fi
	if [[ $lla2 =~ $re ]] ; then
		echo $lla2 > /var/www/html/openWB/ramdisk/llas22
	fi
	if [[ $lla3 =~ $re ]] ; then
		echo $lla3 > /var/www/html/openWB/ramdisk/llas23
	fi
	if [[ $llv1 =~ $re ]] ; then
		echo $llv1 > /var/www/html/openWB/ramdisk/llvs21
	fi
	if [[ $llv2 =~ $re ]] ; then
		echo $llv2 > /var/www/html/openWB/ramdisk/llvs22
	fi
	if [[ $llv3 =~ $re ]] ; then
		echo $llv3 > /var/www/html/openWB/ramdisk/llvs23
	fi

	if [[ $llkwh =~ $rekwh ]] ; then
		echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs2
	fi
	if [[ $evsewifiplugstatelp3 > "1" ]] ; then
		echo 1 > /var/www/html/openWB/ramdisk/plugstatlp3
	else
		echo 0 > /var/www/html/openWB/ramdisk/plugstatlp3
	fi
	if [[ $evsewifiplugstatelp3 > "2" ]] ; then
		echo 1 > /var/www/html/openWB/ramdisk/chargestatlp3
	else
		echo 0 > /var/www/html/openWB/ramdisk/chargestatlp3
	fi
fi
