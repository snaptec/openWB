#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

output=$(curl --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/status)
if [[ $? == "0" ]] ; then
	watt=$(echo $output | jq -r '.nrg[11]')
	watt=$(echo "scale=0;$watt * 10 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		echo $watt > /var/www/html/openWB/ramdisk/llaktuells2
	fi
	lla1=$(echo $output | jq -r '.nrg[4]')
	lla1=$(echo "scale=0;$lla1 / 10" |bc)
	if [[ $lla1 =~ $re ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/llas21
	fi
	lla2=$(echo $output | jq -r '.nrg[5]')
	lla2=$(echo "scale=0;$lla2 / 10" |bc)
	if [[ $lla2 =~ $re ]] ; then
		echo $lla2 > /var/www/html/openWB/ramdisk/llas22
	fi
	lla3=$(echo $output | jq -r '.nrg[6]')
	lla3=$(echo "scale=0;$lla3 / 10" |bc)
	if [[ $lla3 =~ $re ]] ; then
		echo $lla3 > /var/www/html/openWB/ramdisk/llas23
	fi
	llv1=$(echo $output | jq -r '.nrg[0]')
	if [[ $lla1 =~ $re ]] ; then
		echo $llv1 > /var/www/html/openWB/ramdisk/llvs21
	fi
	llv2=$(echo $output | jq -r '.nrg[1]')
	if [[ $lla2 =~ $re ]] ; then
		echo $llv2 > /var/www/html/openWB/ramdisk/llvs22
	fi
	llv3=$(echo $output | jq -r '.nrg[2]')
	if [[ $lla3 =~ $re ]] ; then
		echo $llv3 > /var/www/html/openWB/ramdisk/llvs23
	fi

	llkwh=$(echo $output | jq -r '.eto')
	llkwh=$(echo "scale=3;$llkwh / 10" |bc)
	if [[ $llkwh =~ $rekwh ]] ; then
		echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs2
	fi
fi
