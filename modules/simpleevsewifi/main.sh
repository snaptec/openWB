#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

output=$(curl --connect-timeout $evsewifitimeoutlp1 -s http://$evsewifiiplp1/getParameters)
watt=$(echo $output | jq '.list[] | .actualPower')
lla1=$(echo $output | jq '.list[] | .currentP1')
lla2=$(echo $output | jq '.list[] | .currentP2')
lla3=$(echo $output | jq '.list[] | .currentP3')
evsewifiplugstatelp1=$(echo $output | jq '.list[] | .vehicleState') 
llkwh=$(echo $output | jq '.list[] | .meterReading')
watt=$(echo "scale=0;$watt * 1000 /1" |bc)
if [[ $watt =~ $re ]] ; then
	echo $watt > /var/www/html/openWB/ramdisk/llaktuell
fi
if [[ $lla1 =~ $rekwh ]] ; then
	echo $lla1 > /var/www/html/openWB/ramdisk/lla1
fi
if [[ $lla2 =~ $rekwh ]] ; then
	echo $lla2 > /var/www/html/openWB/ramdisk/lla2
fi
if [[ $lla3 =~ $rekwh ]] ; then
	echo $lla3 > /var/www/html/openWB/ramdisk/lla3
fi
if [[ $llkwh =~ $rekwh ]] ; then
	echo $llkwh > /var/www/html/openWB/ramdisk/llkwh
fi
if [[ $evsewifiplugstatelp1 > "1" ]]; then
        echo 1 > /var/www/html/openWB/ramdisk/plugstat
else
        echo 0 > /var/www/html/openWB/ramdisk/plugstat
fi
if [[ $evsewifiplugstatelp1 > "2" ]] ; then
        echo 1 > /var/www/html/openWB/ramdisk/chargestat
else
	echo 0 > /var/www/html/openWB/ramdisk/chargestat
fi

