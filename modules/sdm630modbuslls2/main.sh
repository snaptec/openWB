#!/bin/bash
if [[ $sdm630lp3source = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$sdm630lp3source,raw tcp:$lllaniplp3:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$sdm630lp3source,raw tcp:$lllaniplp3:26 &
	fi
else
	echo "echo" > /dev/null
fi
n=0
output=$(sudo python /var/www/html/openWB/modules/sdm630modbuslls2/readsdm.py $sdm630lp3source $sdmids2)
while read -r line; do
	if (( $n == 0 )); then
		llas21=$(echo "$line" |  cut -c2- )
		llas21=${llas21%??}
		echo "scale=3; $llas21/1" | bc -l > /var/www/html/openWB/ramdisk/llas21
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llas21
	fi
	if (( $n == 1 )); then
		llas22=$(echo "$line" |  cut -c2- )
		llas22=${llas22%??}
		echo "scale=3; $llas22/1" | bc -l > /var/www/html/openWB/ramdisk/llas22
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llas22
	fi
	if (( $n == 2 )); then
		llas23=$(echo "$line" |  cut -c2- )
		llas23=${llas23%??}
		echo "scale=3; $llas23/1" | bc -l > /var/www/html/openWB/ramdisk/llas23
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llas23
	fi
	if (( $n == 3 )); then
		wl1=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 4 )); then
		llkwhs2=$(echo "$line" |  cut -c2- )
		llkwhs2=${llkwhs2%??}
		rekwh='^[-+]?[0-9]+\.?[0-9]*$'
		if [[ $llkwhs2 =~ $rekwh ]]; then 
			echo "scale=3; $llkwhs2/1" | bc -l > /var/www/html/openWB/ramdisk/llkwhs2
		fi
	fi
	if (( $n == 5 )); then
		wl2=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 6 )); then
		wl3=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 7 )); then
		llvs21=$(echo "$line" |  cut -c2- )
		llvs21=${llvs21%??}
		echo "scale=3; $llvs21/1" | bc -l > /var/www/html/openWB/ramdisk/llvs21
		# LANG=C printf "%.1f\n" $llvs21 > /var/www/html/openWB/ramdisk/llvs21
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llvs21
	fi
	if (( $n == 8 )); then
		llvs22=$(echo "$line" |  cut -c2- )
		llvs22=${llvs22%??}
		echo "scale=3; $llvs22/1" | bc -l > /var/www/html/openWB/ramdisk/llvs22
		# LANG=C printf "%.1f\n" $llvs22 > /var/www/html/openWB/ramdisk/llvs22
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llvs22
	fi
	if (( $n == 9 )); then
		llvs23=$(echo "$line" |  cut -c2- )
		llvs23=${llvs23%??}
		echo "scale=3; $llvs23/1" | bc -l > /var/www/html/openWB/ramdisk/llvs23
		# LANG=C printf "%.1f\n" $llvs23 > /var/www/html/openWB/ramdisk/llvs23
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llvs23
	fi
	n=$((n + 1))
done <<< "$output"

re='^-?[0-9]+$'
if [[ $wl1 =~ $re ]] && [[ $wl2 =~ $re ]] && [[ $wl3 =~ $re ]]; then
	llaktuells2=`echo "($wl1+$wl2+$wl3)" |bc`
	echo $llaktuells2 > /var/www/html/openWB/ramdisk/llaktuells2
fi
