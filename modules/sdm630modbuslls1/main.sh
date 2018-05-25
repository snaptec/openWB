#!/bin/bash
. /var/www/html/openWB/openwb.conf

if [[ $evsesources1 = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$evsesources1,raw tcp:$evselanips1:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$evsesources1,raw tcp:$evselanips1:26 &
	fi
else
	echo "echo" > /dev/null
fi
n=0
output=$(sudo python /var/www/html/openWB/modules/sdm630modbuslls1/readsdm.py $evsesources1 $sdmids1)
while read -r line; do
	if (( $n == 0 )); then
		llas11=$(echo "$line" |  cut -c2- )
		llas11=${llas11%??}
		printf "%.2f\n" $llas11 > /var/www/html/openWB/ramdisk/llas11
	fi
	if (( $n == 1 )); then
		llas12=$(echo "$line" |  cut -c2- )
		llas12=${llas12%??}
		printf "%.2f\n" $llas12 > /var/www/html/openWB/ramdisk/llas12
	fi
	if (( $n == 2 )); then
		llas13=$(echo "$line" |  cut -c2- )
		llas13=${llas13%??}
		printf "%.2f\n" $llas13 > /var/www/html/openWB/ramdisk/llas13
	fi
if (( $n == 3 )); then
echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llaktuells1
fi
if (( $n == 4 )); then
	llkwhs1=$(echo "$line" |  cut -c2- )
	       echo ${llkwhs1%??} > /var/www/html/openWB/ramdisk/llkwhs1
fi

n=$((n + 1))
    done <<< "$output"

											
