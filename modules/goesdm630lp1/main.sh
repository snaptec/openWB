#!/bin/bash
. /var/www/html/openWB/openwb.conf
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

output=$(curl --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/status)
if [[ $? == "0" ]] ; then
	watt=$(echo $output | jq -r '.nrg[11]')
	watt=$(echo "scale=0;$watt * 10 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		echo $watt > /dev/null
	fi
	lla1=$(echo $output | jq -r '.nrg[4]')
	lla1=$(echo "scale=0;$lla1 / 10" |bc)
	if [[ $lla1 =~ $re ]] ; then
		echo $lla1 > /dev/null
	fi
	lla2=$(echo $output | jq -r '.nrg[5]')
	lla2=$(echo "scale=0;$lla2 / 10" |bc)
	if [[ $lla2 =~ $re ]] ; then
		echo $lla2 > /dev/null
	fi
	lla3=$(echo $output | jq -r '.nrg[6]')
	lla3=$(echo "scale=0;$lla3 / 10" |bc)
	if [[ $lla3 =~ $re ]] ; then
		echo $lla3 > /dev/null
	fi
	llv1=$(echo $output | jq -r '.nrg[0]')
	if [[ $llv1 =~ $re ]] ; then
		echo $llv1 > /dev/null
	fi
	llv2=$(echo $output | jq -r '.nrg[1]')
	if [[ $llv2 =~ $re ]] ; then
		echo $llv2 > /dev/null
	fi
	llv3=$(echo $output | jq -r '.nrg[2]')
	if [[ $llv3 =~ $re ]] ; then
		echo $llv3 > /dev/null
	fi

	llkwh=$(echo $output | jq -r '.eto')
	llkwh=$(echo "scale=3;$llkwh / 10" |bc)
	if [[ $llkwh =~ $rekwh ]] ; then
		echo $llkwh > /dev/null
	fi
	rfid=$(echo $output | jq -r '.uby')
	oldrfid=$(</var/www/html/openWB/ramdisk/tmpgoelp1rfid)
	if [[ $rfid != $oldrfid ]] ; then
		echo $rfid > /var/www/html/openWB/ramdisk/readtag
		echo $rfid > /var/www/html/openWB/ramdisk/tmpgoelp1rfid
	fi
#car status 1 Ladestation bereit, kein Auto
#car status 2 Auto lädt
#car status 3 Warte auf Fahrzeug
#car status 4 Ladung beendet, Fahrzeug verbunden
    car=$(echo $output | jq -r '.car')
    if [[ $car == "1" ]] ; then
      echo 0 > /var/www/html/openWB/ramdisk/plugstat
    else
      echo 1 > /var/www/html/openWB/ramdisk/plugstat
    fi
    if [[ $car == "2" ]] ; then
      echo 1 > /var/www/html/openWB/ramdisk/chargestat
    else
	      echo 0 > /var/www/html/openWB/ramdisk/chargestat
     fi
fi

#sdm630 abrufen
#if [[ $sdm630modbusllsource = *virtual* ]]
#then
#	if ps ax |grep -v grep |grep "socat pty,link=$sdm630modbusllsource,raw tcp:$goeipsdm630lp1:502" > /dev/null
#	then
#		echo "test" > /dev/null
#	else
#		sudo socat pty,link=$sdm630modbusllsource,raw tcp:$goeipsdm630lp1:502 &
#	fi
#else
#	echo "echo" > /dev/null
#fi
if ping -c 1 $goeipsdm630lp1 > /dev/null
then
    n=0
    output=$(sudo python /var/www/html/openWB/modules/goesdm630lp1/readsdm.py $goeipsdm630lp1 $goeidsdm630lp1)
    while read -r line; do
        if (( $n == 0 )); then
            lla1=$(echo "$line" |  cut -c2- )
            lla1=${lla1%???}
    #		LANG=C printf "%.3f\n" $lla1 > /var/www/html/openWB/ramdisk/lla1
    #		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla1
            echo "scale=3; $lla1/1" | bc -l > /var/www/html/openWB/ramdisk/lla1

        fi
        if (( $n == 1 )); then
            lla2=$(echo "$line" |  cut -c2- )
            lla2=${lla2%???}
    #		LANG=C printf "%.3f\n" $lla2 > /var/www/html/openWB/ramdisk/lla2
    #		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla2
            echo "scale=3; $lla2/1" | bc -l > /var/www/html/openWB/ramdisk/lla2

        fi
        if (( $n == 2 )); then
            lla3=$(echo "$line" |  cut -c2- )
            lla3=${lla3%???}
            echo "scale=3; $lla3/1" | bc -l > /var/www/html/openWB/ramdisk/lla3

    #		LANG=C printf "%.3f\n" $lla3 > /var/www/html/openWB/ramdisk/lla3
    #		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/lla3

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
    #LANG=C printf "%.1f\n" $llv1 > /var/www/html/openWB/ramdisk/llv1
    #		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llv1

    fi
    if (( $n == 8 )); then
    llv2=$(echo "$line" |  cut -c2- )
    llv2=${llv2%???}
    echo "scale=1; $llv2/1" | bc -l > /var/www/html/openWB/ramdisk/llv2
    #LANG=C printf "%.1f\n" $llv2 > /var/www/html/openWB/ramdisk/llv2
    #echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llv2
    fi
    if (( $n == 9 )); then
    llv3=$(echo "$line" |  cut -c2- )
    llv3=${llv3%???}
    echo "scale=1; $llv3/1" | bc -l > /var/www/html/openWB/ramdisk/llv3
    #LANG=C printf "%.1f\n" $llv3 > /var/www/html/openWB/ramdisk/llv3
    #		echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llv3
    fi
    if (( $n == 10 )); then
    #echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llaltnv
    #llaltnv=$(echo "$line" |  cut -c2- )
    #llaltnv=${llaltnv%??}
    #printf "%.1f\n" $llaltnv > /var/www/html/openWB/ramdisk/llaltnv
            echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llaltnv
    fi
    if (( $n == 11 )); then
    #	llhz=$(echo "$line" |  cut -c2- )
    #	llhz=${llhz%??} 
    #       printf "%.1f\n" $llhz > /var/www/html/openWB/ramdisk/llhz
            echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/llhz
    echo "$line" |  cut -c2- |sed 's/\..*$//' > /var/www/html/openWB/ramdisk/evuhz

    fi
    if (( $n == 12 )); then
    llpf1=$(echo "$line" |  cut -c2- )
    llpf1=${llpf1%??}
    echo "scale=3; $llpf1/1" | bc -l > /var/www/html/openWB/ramdisk/llpf1
    #LANG=C printf "%.3f\n" $llpf1 > /var/www/html/openWB/ramdisk/llpf1

    fi
    if (( $n == 13 )); then
    llpf2=$(echo "$line" |  cut -c2- )
    llpf2=${llpf2%??}
    echo "scale=3; $llpf2/1" | bc -l > /var/www/html/openWB/ramdisk/llpf2
    #LANG=C printf "%.3f\n" $llpf2 > /var/www/html/openWB/ramdisk/llpf2
    fi
    if (( $n == 14 )); then
    llpf3=$(echo "$line" |  cut -c2- )
    llpf3=${llpf3%??}
    echo "scale=3; $llpf3/1" | bc -l > /var/www/html/openWB/ramdisk/llpf3
    #LANG=C printf "%.3f\n" $llpf3 > /var/www/html/openWB/ramdisk/llpf3
    fi


        n=$((n + 1))
        done <<< "$output"


        
    re='^-?[0-9]+$'
    if [[ $wl1 =~ $re ]] && [[ $wl2 =~ $re ]] && [[ $wl3 =~ $re ]]; then
        llaktuell=`echo "($wl1+$wl2+$wl3)" |bc`
        #Grundrauschen des GOE-Chargers bei nicht laden nicht anzeigen.
        if [ $llaktuell == 6 ]; then
        echo 0 >/var/www/html/openWB/ramdisk/llaktuell
        elif [ $llaktuell == 5 ]; then
        echo 0 > /var/www/html/openWB/ramdisk/llaktuell
        else 
        echo $llaktuell > /var/www/html/openWB/ramdisk/llaktuell
        fi
    fi
fi
