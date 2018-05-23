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
		bezugkwh=$(echo "$line" |  cut -c2- )
#		echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/bezugkwh
#		echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/einspeisungkwh
	fi
	if (( $n == 7 )); then
	ikwh1=$(echo "$line" |  cut -c2- )
	fi
	if (( $n == 8 )); then
	ikwh2=$(echo "$line" |  cut -c2- )
	fi
	if (( $n == 9 )); then
	ikwh3=$(echo "$line" |  cut -c2- )
	fi
	if (( $n == 10 )); then
	ekwh1=$(echo "$line" |  cut -c2- )
	fi
	if (( $n == 11 )); then
	ekwh2=$(echo "$line" |  cut -c2- )
	fi
	if (( $n == 12 )); then
	ekwh3=$(echo "$line" |  cut -c2- )
	fi
	if (( $n == 13 )); then
		evupf1=$(echo "$line" |  cut -c2- )
		echo ${evupf1%??} > /var/www/html/openWB/ramdisk/evupf1
	fi
	if (( $n == 14 )); then
		evupf2=$(echo "$line" |  cut -c2- )
		echo ${evupf2%??} > /var/www/html/openWB/ramdisk/evupf2
	fi
	if (( $n == 15 )); then
		evupf3=$(echo "$line" |  cut -c2- )
		echo ${evupf3%??} > /var/www/html/openWB/ramdisk/evupf3
	fi
	if (( $n == 16 )); then
		evuv1=$(echo "$line" |  cut -c2- )
		echo ${evuv1%??} > /var/www/html/openWB/ramdisk/evuv1
	fi
	if (( $n == 17 )); then
		evuv2=$(echo "$line" |  cut -c2- )
		echo ${evuv2%??} > /var/www/html/openWB/ramdisk/evuv2
	fi
	if (( $n == 18 )); then
		evuv3=$(echo "$line" |  cut -c2- )
		echo ${evuv3%??} > /var/www/html/openWB/ramdisk/evuv3
	fi
	if (( $n == 19 )); then
		llhz=$(echo "$line" |  cut -c2- )
		echo ${llhz%??} > /var/www/html/openWB/ramdisk/llhz
	fi


	n=$((n + 1))
done <<< "$output"



wattbezug=`echo "($wl1+$wl2+$wl3)" |bc`
echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
ikwh11=${ikwh1%??}
ikwh22=${ikwh2%??}
ikwh33=${ikwh3%??}
echo $ikwh11 > /var/www/html/openWB/ramdisk/bezugkwh1
echo $ikwh22 > /var/www/html/openWB/ramdisk/bezugkwh2
echo $ikwh33 > /var/www/html/openWB/ramdisk/bezugkwh3

ikwh=$(echo "(($ikwh11+$ikwh22+$ikwh33)*1000)" |bc)
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
ekwh11=${ekwh1%??}
ekwh22=${ekwh2%??}
ekwh33=${ekwh3%??}
echo $ekwh11 > /var/www/html/openWB/ramdisk/einspeisungkwh1
echo $ekwh22 > /var/www/html/openWB/ramdisk/einspeisungkwh2
echo $ekwh33 > /var/www/html/openWB/ramdisk/einspeisungkwh3

ekwh=$(echo "(($ekwh11+$ekwh22+$ekwh33)*1000)" |bc)
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh


#echo ${ikwh2%??}
#echo ${ikwh3%??}

