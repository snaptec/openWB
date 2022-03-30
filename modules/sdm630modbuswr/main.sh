#!/bin/bash
if [[ $sdm630modbuswrsource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$sdm630modbuswrsource,raw tcp:$sdm630modbuswrlanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$sdm630modbuswrsource,raw tcp:$sdm630modbuswrlanip:26 &
	fi
else
	echo "echo" > /dev/null
fi
n=0
output=$(sudo python /var/www/html/openWB/modules/sdm630modbuswr/readsdm.py $sdm630modbuswrsource $sdm630modbuswrid)
while read -r line; do
	if (( $n == 0 )); then
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/wra1
	fi
	if (( $n == 1 )); then
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/wra2
	fi
	if (( $n == 2 )); then
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/wra3
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
		wrkwh=$(echo "$line" |  cut -c2- )
		wrkwh=${wrkwh%??}
		wrwh=$(echo "$wrkwh * 1000" |bc)
		echo $wrwh > /var/www/html/openWB/ramdisk/pvkwh
		LANG=C printf "%.4f\n" $wrkwh > /var/www/html/openWB/ramdisk/pvkwhk
	fi
	n=$((n + 1))
done <<< "$output"

wattwr=`echo "(($wl1+$wl2+$wl3)* -1)" |bc`
if (( wattwr > 0 )); then
	wattwr=$(echo "$wattwr * -1" |bc)
fi
echo $wattwr
echo $wattwr > /var/www/html/openWB/ramdisk/pvwatt
