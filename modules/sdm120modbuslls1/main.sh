#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

if [[ $sdm120lp2source = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$sdm120lp2source,raw tcp:$lllaniplp2:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$sdm120lp2source,raw tcp:$lllaniplp2:26 &
	fi
else
	echo "echo" > /dev/null
fi

if [[ $sdm120modbusllid1s1 != "254" ]] && [[ $sdm120modbusllid2s1 != "254" ]] && [[ $sdm120modbusllid3s1 != "254" ]] ; then
	n=0
	output=$(sudo python /var/www/html/openWB/modules/sdm120modbuslls1/readsdm3.py $sdm120lp2source $sdm120modbusllid1s1 $sdm120modbusllid2s1 $sdm120modbusllid3s1)
	while read -r line; do
		if (( $n == 0 )); then
			llv1=$(echo "$line" |  cut -c2- )
			llv1=${llv1%??}
			LANG=C printf "%.1f\n" $llv1 > /var/www/html/openWB/ramdisk/llvs11
		fi
		if (( $n == 1 )); then
			lla1=$(echo "$line" |  cut -c2- )
			lla1=${lla1%??}
			LANG=C printf "%.3f\n" $lla1 > /var/www/html/openWB/ramdisk/llas11
		fi
		if (( $n == 2 )); then
			wl1=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
		fi
		if (( $n == 3 )); then
			llpf1=$(echo "$line" |  cut -c2- )
			llpf1=${llpf1%??}
			LANG=C printf "%.3f\n" $llpf1 > /var/www/html/openWB/ramdisk/llpfs11
		fi
		if (( $n == 4 )); then
			llkwh=$(echo "$line" |  cut -c2- )
			llkwh=${llkwh%???}
		fi
		if (( $n == 5 )); then
			llv2=$(echo "$line" |  cut -c2- )
			llv2=${llv2%??}
			LANG=C printf "%.1f\n" $llv2 > /var/www/html/openWB/ramdisk/llvs12
		fi
		if (( $n == 6 )); then
			lla2=$(echo "$line" |  cut -c2- )
			lla2=${lla2%??}
			LANG=C printf "%.3f\n" $lla2 > /var/www/html/openWB/ramdisk/llas12
		fi
		if (( $n == 7 )); then
			wl2=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
		fi
		if (( $n == 8 )); then
			llpf2=$(echo "$line" |  cut -c2- )
			llpf2=${llpf2%??}
			LANG=C printf "%.3f\n" $llpf2 > /var/www/html/openWB/ramdisk/llpfs12
		fi
		if (( $n == 9 )); then
			llkwh2=$(echo "$line" |  cut -c2- )
			llkwh2=${llkwh2%???}
		fi
		if (( $n == 10 )); then
			llv3=$(echo "$line" |  cut -c2- )
			llv3=${llv3%??}
			LANG=C printf "%.1f\n" $llv3 > /var/www/html/openWB/ramdisk/llvs13
		fi
		if (( $n == 11 )); then
			lla3=$(echo "$line" |  cut -c2- )
			lla3=${lla3%??}
			LANG=C printf "%.3f\n" $lla3 > /var/www/html/openWB/ramdisk/llas13
		fi
		if (( $n == 12 )); then
			wl3=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
		fi
		if (( $n == 13 )); then
			llpf3=$(echo "$line" |  cut -c2- )
			llpf3=${llpf3%??}
			LANG=C printf "%.3f\n" $llpf3 > /var/www/html/openWB/ramdisk/llpfs13
		fi
		if (( $n == 14 )); then
			llkwh3=$(echo "$line" |  cut -c2- )
			llkwh3=${llkwh3%???}
			fi
		n=$((n + 1))
	done <<< "$output"
	if [[ $llkwh =~ $rekwh ]] && [[ $llkwh2 =~ $rekwh ]] && [[ $llkwh3 =~ $rekwh ]]; then
		lltotal=`echo "($llkwh+$llkwh2+$llkwh3)" |bc`
		LANG=C printf "%.3f\n" $lltotal > /var/www/html/openWB/ramdisk/llkwhs1
	fi
	if [[ $wl1 =~ $re ]] && [[ $wl2 =~ $re ]] && [[ $wl3 =~ $re ]]; then
	 	llaktuell=`echo "($wl1+$wl2+$wl3)" |bc`
		echo $llaktuell > /var/www/html/openWB/ramdisk/llaktuells1
	fi
else
	if [[ $sdm120modbusllid2s1 != "254" ]] ; then
		n=0
		output=$(sudo python /var/www/html/openWB/modules/sdm120modbuslls1/readsdm2.py $sdm120lp2source $sdm120modbusllid1s1 $sdm120modbusllid2s1)
		while read -r line; do
			if (( $n == 0 )); then
				llv1=$(echo "$line" |  cut -c2- )
				llv1=${llv1%??}
				LANG=C printf "%.1f\n" $llv1 > /var/www/html/openWB/ramdisk/llvs11
			fi
			if (( $n == 1 )); then
				lla1=$(echo "$line" |  cut -c2- )
				lla1=${lla1%??}
				LANG=C printf "%.3f\n" $lla1 > /var/www/html/openWB/ramdisk/llas11
			fi
			if (( $n == 2 )); then
				wl1=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
				fi
			if (( $n == 3 )); then
				llpf1=$(echo "$line" |  cut -c2- )
				llpf1=${llpf1%??}
				LANG=C printf "%.3f\n" $llpf1 > /var/www/html/openWB/ramdisk/llpfs11
			fi
			if (( $n == 4 )); then
				llkwh=$(echo "$line" |  cut -c2- )
				llkwh=${llkwh%???}
			fi
			n=$((n + 1))
		done <<< "$output"
		if [[ $llkwh =~ $rekwh ]] ; then
			lltotal=`echo "($llkwh)" |bc`
			LANG=C printf "%.3f\n" $lltotal > /var/www/html/openWB/ramdisk/llkwhs1
		fi
		if [[ $wl1 =~ $re ]]; then
		 	llaktuell=`echo "($wl1)" |bc`
			echo $llaktuell > /var/www/html/openWB/ramdisk/llaktuells1
		fi
	else
		sudo python /var/www/html/openWB/modules/sdm120modbuslls1/readsdm1.py $sdm120lp2source $sdm120modbusllid1s1
	fi
fi
