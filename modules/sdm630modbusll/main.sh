#!/bin/bash
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
		lla1=$(echo "$line" |  cut -c2- )
		lla1=${lla1%???}
		# LANG=C printf "%.3f\n" $lla1 > /var/www/html/openWB/ramdisk/lla1
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla1
		echo "scale=3; $lla1/1" | bc -l > /var/www/html/openWB/ramdisk/lla1
	fi
	if (( $n == 1 )); then
		lla2=$(echo "$line" |  cut -c2- )
		lla2=${lla2%???}
		# LANG=C printf "%.3f\n" $lla2 > /var/www/html/openWB/ramdisk/lla2
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla2
		echo "scale=3; $lla2/1" | bc -l > /var/www/html/openWB/ramdisk/lla2
	fi
	if (( $n == 2 )); then
		lla3=$(echo "$line" |  cut -c2- )
		lla3=${lla3%???}
		echo "scale=3; $lla3/1" | bc -l > /var/www/html/openWB/ramdisk/lla3
		# LANG=C printf "%.3f\n" $lla3 > /var/www/html/openWB/ramdisk/lla3
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla3
	fi
	if (( $n == 3 )); then
		wl1=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 4 )); then
		llkwh=$(echo "$line" |  cut -c2- )
		llkwh=${llkwh%???}
		rekwh='^[-+]?[0-9]+\.?[0-9]*$'
		if [[ $llkwh =~ $rekwh ]]; then 
			#LANG=C printf "%.3f\n" $llkwh > /var/www/html/openWB/ramdisk/llkwh
			echo "scale=3; $llkwh/1" | bc -l > /var/www/html/openWB/ramdisk/llkwh
		fi
	fi
	if (( $n == 5 )); then
		wl2=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 6 )); then
		wl3=$(echo "$line" |  cut -c2- |sed 's/\..*$//')
	fi
	if (( $n == 7 )); then
	llv1=$(echo "$line" |  cut -c2- )
	llv1=${llv1%???}
	echo "scale=1; $llv1/1" | bc -l > /var/www/html/openWB/ramdisk/llv1
	# LANG=C printf "%.1f\n" $llv1 > /var/www/html/openWB/ramdisk/llv1
	# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llv1
	fi
	if (( $n == 8 )); then
	llv2=$(echo "$line" |  cut -c2- )
	llv2=${llv2%???}
	echo "scale=1; $llv2/1" | bc -l > /var/www/html/openWB/ramdisk/llv2
	# LANG=C printf "%.1f\n" $llv2 > /var/www/html/openWB/ramdisk/llv2
	# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llv2
	fi
	if (( $n == 9 )); then
	llv3=$(echo "$line" |  cut -c2- )
	llv3=${llv3%???}
	echo "scale=1; $llv3/1" | bc -l > /var/www/html/openWB/ramdisk/llv3
	# LANG=C printf "%.1f\n" $llv3 > /var/www/html/openWB/ramdisk/llv3
	# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llv3
	fi
	if (( $n == 10 )); then
		# echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llaltnv
		# llaltnv=$(echo "$line" |  cut -c2- )
		# llaltnv=${llaltnv%??}
		# printf "%.1f\n" $llaltnv > /var/www/html/openWB/ramdisk/llaltnv
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llaltnv
	fi
	if (( $n == 11 )); then
		# llhz=$(echo "$line" |  cut -c2- )
		# llhz=${llhz%??} 
		# printf "%.1f\n" $llhz > /var/www/html/openWB/ramdisk/llhz
		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llhz
	fi
	if (( $n == 12 )); then
		llpf1=$(echo "$line" |  cut -c2- )
		llpf1=${llpf1%??}
		echo "scale=3; $llpf1/1" | bc -l > /var/www/html/openWB/ramdisk/llpf1
		# LANG=C printf "%.3f\n" $llpf1 > /var/www/html/openWB/ramdisk/llpf1
	fi
	if (( $n == 13 )); then
		llpf2=$(echo "$line" |  cut -c2- )
		llpf2=${llpf2%??}
		echo "scale=3; $llpf2/1" | bc -l > /var/www/html/openWB/ramdisk/llpf2
		# LANG=C printf "%.3f\n" $llpf2 > /var/www/html/openWB/ramdisk/llpf2
	fi
	if (( $n == 14 )); then
		llpf3=$(echo "$line" |  cut -c2- )
		llpf3=${llpf3%??}
		echo "scale=3; $llpf3/1" | bc -l > /var/www/html/openWB/ramdisk/llpf3
		# LANG=C printf "%.3f\n" $llpf3 > /var/www/html/openWB/ramdisk/llpf3
	fi
	n=$((n + 1))
done <<< "$output"

re='^-?[0-9]+$'
if [[ $wl1 =~ $re ]] && [[ $wl2 =~ $re ]] && [[ $wl3 =~ $re ]]; then
	llaktuell=`echo "($wl1+$wl2+$wl3)" |bc`
	echo $llaktuell > /var/www/html/openWB/ramdisk/llaktuell
fi
