#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

output=$(curl --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/status)
if [[ $? == "0" ]] ; then
	watt=$(echo $output | jq -r '.nrg[11]')
	watt=$(echo "scale=0;$watt * 10 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		echo $watt > /var/www/html/openWB/ramdisk/llaktuells2
	fi
	lla1=$(echo $output | jq -r '.nrg[4]')
	lla1=$(echo "scale=0;$lla1 / 10" |bc)
	if [[ $lla1 =~ $re ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/llas21
	fi
	lla2=$(echo $output | jq -r '.nrg[5]')
	lla2=$(echo "scale=0;$lla2 / 10" |bc)
	if [[ $lla2 =~ $re ]] ; then
		echo $lla2 > /var/www/html/openWB/ramdisk/llas22
	fi
	lla3=$(echo $output | jq -r '.nrg[6]')
	lla3=$(echo "scale=0;$lla3 / 10" |bc)
	if [[ $lla3 =~ $re ]] ; then
		echo $lla3 > /var/www/html/openWB/ramdisk/llas23
	fi
	llv1=$(echo $output | jq -r '.nrg[0]')
	if [[ $llv1 =~ $re ]] ; then
		echo $llv1 > /var/www/html/openWB/ramdisk/llvs21
	fi
	llv2=$(echo $output | jq -r '.nrg[1]')
	if [[ $llv2 =~ $re ]] ; then
		echo $llv2 > /var/www/html/openWB/ramdisk/llvs22
	fi
	llv3=$(echo $output | jq -r '.nrg[2]')
	if [[ $llv3 =~ $re ]] ; then
		echo $llv3 > /var/www/html/openWB/ramdisk/llvs23
	fi
	llkwh=$(echo $output | jq -r '.eto')
	llkwh=$(echo "scale=3;$llkwh / 10" |bc)
	#if [[ $llkwh =~ $rekwh ]] ; then
	#	echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs2	
    #fi
    
    #simulation der Energiemenge während des ladens
	#wenn die Dateien noch nicht da sind, werden sie angelegt sobald das Auto nicht angesteckt ist.
	if [ -f "/var/www/html/openWB/ramdisk/goe3watt0neg" ]; then
		if [ -f "/var/www/html/openWB/ramdisk/goe3watt0pos" ]; then
			python /var/www/html/openWB/runs/simcount.py $watt goe3 goe3poskwh goe3negkwh
		fi
	fi    
    
	#car status 1 Ladestation bereit, kein Auto
	#car status 2 Auto lädt
	#car status 3 Warte auf Fahrzeug
	#car status 4 Ladung beendet, Fahrzeug verbunden
	car=$(echo $output | jq -r '.car')
	if [[ $car == "1" ]] ; then
		echo 0 > /var/www/html/openWB/ramdisk/plugstatlp3
        #wenn das Auto nicht angesteckt ist, wird der simulierte Zählerstand mit dem ausgelesenen Zählerstand überschrieben
		#Damit wird die Simulation wieder mit dem Zähler des Go-E abgeglichen, die Nachkommestellen gehen allerdings verloren.
		echo 0 > /var/www/html/openWB/ramdisk/goe3watt0neg
		if [[ $llkwh =~ $rekwh ]] ; then
			echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs2
			simenergy=$(echo "scale=0; $(</var/www/html/openWB/ramdisk/llkwhs2)*3600000/1" | bc)
			echo $simenergy > /var/www/html/openWB/ramdisk/goe3watt0pos
		fi
	else
		echo 1 > /var/www/html/openWB/ramdisk/plugstatlp3
        #wenn das Auto angesteckt ist, wird der ausgelesene Zählerstand ignoriert und stattdessen die Leistung aufintegriert
		#Grund: der ausgelesene Zählerstand hat eine Auflösung von 1kWh -> zu ungenau in der Darstellung
		if [ -f "/var/www/html/openWB/ramdisk/goe3poskwh" ]; then
            simenergy=$(echo "scale=3; $(</var/www/html/openWB/ramdisk/goe3poskwh)/1000" | bc)
		    echo $simenergy > /var/www/html/openWB/ramdisk/llkwhs2
        else
            echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs2
        fi
	fi
	if [[ $car == "2" ]] ; then
		echo 1 > /var/www/html/openWB/ramdisk/chargestatlp3
	else
		echo 0 > /var/www/html/openWB/ramdisk/chargestatlp3
	fi
fi
