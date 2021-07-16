#!/bin/bash
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
		evua1=$(echo "$line" |  cut -c2- )
		evua1=${evua1%??}
		echo "scale=3; $evua1/1" | bc -l > /var/www/html/openWB/ramdisk/bezuga1
		# LANG=C printf "%.3f\n" $evua1 > /var/www/html/openWB/ramdisk/bezuga1
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/bezuga1
	fi
	if (( $n == 1 )); then
		evua2=$(echo "$line" |  cut -c2- )
		evua2=${evua2%??}
		echo "scale=3; $evua2/1" | bc -l > /var/www/html/openWB/ramdisk/bezuga2
		# LANG=C printf "%.3f\n" $evua2 > /var/www/html/openWB/ramdisk/bezuga2
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/bezuga2
	fi
	if (( $n == 2 )); then
		evua3=$(echo "$line" |  cut -c2- )
		evua3=${evua3%??}
		echo "scale=3; $evua3/1" | bc -l > /var/www/html/openWB/ramdisk/bezuga3
		# LANG=C printf "%.3f\n" $evua3 > /var/www/html/openWB/ramdisk/bezuga3
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/bezuga3
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
		bezugkwhold=$(echo "$line" |  cut -c2- )
		# echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/bezugkwh
		# echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/einspeisungkwh
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
		evupf1=${evupf1%??}
		echo "scale=3; $evupf1/1" | bc -l > /var/www/html/openWB/ramdisk/evupf1
		# LANG=C printf "%.3f\n" $evupf1 > /var/www/html/openWB/ramdisk/evupf1
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evupf1
	fi
	if (( $n == 14 )); then
		evupf2=$(echo "$line" |  cut -c2- )
		evupf2=${evupf2%??} 
		echo "scale=3; $evupf2/1" | bc -l > /var/www/html/openWB/ramdisk/evupf2
		# LANG=C printf "%.3f\n" $evupf2  > /var/www/html/openWB/ramdisk/evupf2
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evupf2
	fi
	if (( $n == 15 )); then
		evupf3=$(echo "$line" |  cut -c2- )
		evupf3=${evupf3%??} 
		echo "scale=3; $evupf3/1" | bc -l > /var/www/html/openWB/ramdisk/evupf3
		# LANG=C printf "%.3f\n" $evupf3  > /var/www/html/openWB/ramdisk/evupf3
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evupf3
	fi
	if (( $n == 16 )); then
		evuv1=$(echo "$line" |  cut -c2- )
		evuv1=${evuv1%??}
		echo "scale=3; $evuv1/1" | bc -l > /var/www/html/openWB/ramdisk/evuv1
		# LANG=C printf "%.1f\n" $evuv1 > /var/www/html/openWB/ramdisk/evuv1
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evuv1
	fi
	if (( $n == 17 )); then
		evuv2=$(echo "$line" |  cut -c2- )
		evuv2=${evuv2%??}
		echo "scale=3; $evuv2/1" | bc -l > /var/www/html/openWB/ramdisk/evuv2
		# LANG=C printf "%.1f\n" $evuv2 > /var/www/html/openWB/ramdisk/evuv2
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evuv2
	fi
	if (( $n == 18 )); then
		evuv3=$(echo "$line" |  cut -c2- )
		evuv3=${evuv3%??}
		echo "scale=3; $evuv3/1" | bc -l > /var/www/html/openWB/ramdisk/evuv3
		# LANG=C printf "%.1f\n" $evuv3 > /var/www/html/openWB/ramdisk/evuv3
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evuv3
	fi
	if (( $n == 19 )); then
		evuhz=$(echo "$line" |  cut -c2- )
		evuhz=${evuhz%??}
		echo "scale=3; $evuhz/1" | bc -l > /var/www/html/openWB/ramdisk/evuhz
		# LANG=C printf "%.2f\n" $evuhz > /var/www/html/openWB/ramdisk/evuhz
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evuhz
	fi
	if (( $n == 20 )); then
		bezugkwh=$(echo "$line" |  cut -c2- )
		# echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/bezugkwh
		# echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/einspeisungkwh
	fi
	if (( $n == 21 )); then
		einspeisungkwh=$(echo "$line" |  cut -c2- )
		# echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/bezugkwh
		# echo ${bezugkwh%??} > /var/www/html/openWB/ramdisk/einspeisungkwh
	fi
	n=$((n + 1))
done <<< "$output"

wattbezug=`echo "($wl1+$wl2+$wl3)" |bc`
echo $wl1 > /var/www/html/openWB/ramdisk/bezugw1
echo $wl2 > /var/www/html/openWB/ramdisk/bezugw2
echo $wl3 > /var/www/html/openWB/ramdisk/bezugw3

echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
ikwh11=${ikwh1%??}
ikwh22=${ikwh2%??}
ikwh33=${ikwh3%??}
echo $ikwh11 > /var/www/html/openWB/ramdisk/bezugkwh1
echo $ikwh22 > /var/www/html/openWB/ramdisk/bezugkwh2
echo $ikwh33 > /var/www/html/openWB/ramdisk/bezugkwh3
bezugkwh=${bezugkwh%??}
einspeisungkwh=${einspeisungkwh%??}
einspeisungkwh=$(echo "(($einspeisungkwh)*1000)" | bc)
rekwh='^[-+]?[0-9]+\.?[0-9]*$'
if [[ $bezugkwh =~ $rekwh ]]; then
	bezugkwh=$(echo "(($bezugkwh)*1000)" | bc)
	# LANG=C printf "%.3f\n" $bezugkwh > /var/www/html/openWB/ramdisk/bezugkwh
	echo "scale=3; $bezugkwh/1" | bc -l > /var/www/html/openWB/ramdisk/bezugkwh
fi
ekwh11=${ekwh1%??}
ekwh22=${ekwh2%??}
ekwh33=${ekwh3%??}
echo $ekwh11 > /var/www/html/openWB/ramdisk/einspeisungkwh1
echo $ekwh22 > /var/www/html/openWB/ramdisk/einspeisungkwh2
echo $ekwh33 > /var/www/html/openWB/ramdisk/einspeisungkwh3

# ekwh=$(echo "(($ekwh11+$ekwh22+$ekwh33)*1000)" |bc)

if [[ $einspeisungkwh =~ $rekwh ]]; then 
	echo $einspeisungkwh > /var/www/html/openWB/ramdisk/einspeisungkwh
fi

# echo ${ikwh2%??}
# echo ${ikwh3%??}
