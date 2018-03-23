#!/bin/bash
. /var/www/html/openWB/openwb.conf

if [[ $sdm630modbusllsource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$sdm630modbusllsource,raw tcp:$sdm630modbuslllanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$sdm630modbusllsource,raw tcp:$sdm630modbuslllanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
n=0
output=$(sudo python /var/www/html/openWB/modules/sdm630modbusll/readsdm.py $sdm630modbusllsource $sdm630modbusllid)
while read -r line; do

if (( $n == 0 )); then
echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla1
fi
if (( $n == 1 )); then
echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla2
fi
if (( $n == 2 )); then
echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla3
fi
if (( $n == 3 )); then
echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llaktuell
fi
n=$((n + 1))
    done <<< "$output"

											
