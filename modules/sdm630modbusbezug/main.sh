#!/bin/bash

. /var/www/html/openWB/openwb.conf

if [[ $sdm630modbusbezugsource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$sdm630modbusbezugsource,raw tcp:$sdm630modbusbezuglanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$sdm630modbusbezugsource,raw tcp:$sdm630modbusbezuglanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
n=0
output=$(sudo python /var/www/html/openWB/modules/sdm630modbusbezug/readsdm.py $sdm630modbusbezugsource $sdm630modbusbezugid)
while read -r line; do
	if (( $n == 0 )); then
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/bezuga1
	fi
	if (( $n == 1 )); then
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/bezuga2
	fi
	if (( $n == 2 )); then
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/bezuga3
	fi
	if (( $n == 3 )); then
		wl1=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 4 )); then
		wl2=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 5 )); then
		wl3=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 6 )); then
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/bezugkwh
	fi

	n=$((n + 1))
done <<< "$output"

wattbezug=`echo "($wl1+wl2+$wl3)" |bc`
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug



