#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

if [[ $modbusevsesource = *virtual* ]]
then
	if ps ax |grep -v grep |grep "socat pty,link=$sdm120modbusllsource,raw tcp:$sdm630modbuslllanip:26" > /dev/null
	then
		echo "test" > /dev/null
	else
		sudo socat pty,link=$sdm120modbusllsource,raw tcp:$sdm630modbuslllanip:26 &
	fi
else
	echo "echo" > /dev/null
fi

if [[ $sdm120modbusllid1 != "none" ]] && [[ $sdm120modbusllid2 != "254" ]] && [[ $sdm120modbusllid3 != "254" ]] ; then
	n=0
	output=$(sudo python /var/www/html/openWB/modules/sdm120modbusll/readsdm3.py $sdm120modbusllsource $sdm120modbusllid1 $sdm120modbusllid2 $sdm120modbusllid3)

else
	if [[ $sdm120modbusllid2 != "254" ]] ; then
		n=0
		output=$(sudo python /var/www/html/openWB/modules/sdm120modbusll/readsdm2.py $sdm120modbusllsource $sdm120modbusllid1 $sdm120modbusllid2)
		while read -r line; do
			if (( $n == 0 )); then
				llv1=$(echo "$line" |  cut -c2- )
				llv1=${llv1%??}
				LANG=C printf "%.1f\n" $llv1 > /var/www/html/openWB/ramdisk/llv1
			fi
			if (( $n == 1 )); then
				lla1=$(echo "$line" |  cut -c2- )
				lla1=${lla1%??}
				LANG=C printf "%.3f\n" $lla1 > /var/www/html/openWB/ramdisk/lla1
			fi
			if (( $n == 2 )); then
				wl1=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
				fi
			if (( $n == 3 )); then
				llpf1=$(echo "$line" |  cut -c2- )
				llpf1=${llpf1%??}
				LANG=C printf "%.3f\n" $llpf1 > /var/www/html/openWB/ramdisk/llpf1
			fi
			if (( $n == 4 )); then
				llkwh=$(echo "$line" |  cut -c2- )
				llkwh=${llkwh%???}
			fi
			n=$((n + 1))
		done <<< "$output"
		if [[ $llkwh =~ $rekwh ]] ; then
			lltotal=`echo "($llkwh)" |bc`
			LANG=C printf "%.3f\n" $lltotal > /var/www/html/openWB/ramdisk/llkwh
		fi
		if [[ $wl1 =~ $re ]]; then
			llaktuell=`echo "($wl1)" |bc`
			echo $llaktuell > /var/www/html/openWB/ramdisk/llaktuell
		fi
	else
		sudo python /var/www/html/openWB/modules/sdm120modbusll/readsdm1.py $sdm120modbusllsource $sdm120modbusllid1
	fi
fi
