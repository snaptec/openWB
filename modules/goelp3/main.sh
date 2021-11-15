#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

output=$(curl --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/status)
if [[ $? == "0" ]] ; then
	goecorrectionfactor=$(echo "scale=0;$goecorrectionfactorlp3 * 100000 /1" |bc)
	watt=$(echo $output | jq -r '.nrg[11]')
	watt=$(echo "scale=0;$watt * 10 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		if [[ $goesimulationlp1 == "0" ]] ; then
			echo $watt > /var/www/html/openWB/ramdisk/llaktuells2
		else
			wattc=$((watt*$goecorrectionfactor/100000))
			wattc=$(echo "scale=0;$wattc" |bc)
			echo $wattc > /var/www/html/openWB/ramdisk/llaktuells2
		fi
	fi
	lla1=$(echo $output | jq -r '.nrg[4]')
	lla1=$(echo "scale=1;$lla1 / 10" |bc)
	if [[ $lla1 =~ $rekwh ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/llas21
	fi
	lla2=$(echo $output | jq -r '.nrg[5]')
	lla2=$(echo "scale=1;$lla2 / 10" |bc)
	if [[ $lla2 =~ $rekwh ]] ; then
		echo $lla2 > /var/www/html/openWB/ramdisk/llas22
	fi
	lla3=$(echo $output | jq -r '.nrg[6]')
	lla3=$(echo "scale=1;$lla3 / 10" |bc)
	if [[ $lla3 =~ $rekwh ]] ; then
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
	if [[ $goesimulationlp3 == "0" ]] ; then
		if [[ $llkwh =~ $rekwh ]] ; then
			echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs2
		fi
	else	
		temp_kWhCounter_lp3=$(</var/www/html/openWB/ramdisk/temp_kWhCounter_lp3)
		#simulation der Energiemenge während des ladens
		#wenn die Dateien noch nicht da sind, werden sie angelegt. Simulation startet im nächsten Regelschritt.
		if [ -f "/var/www/html/openWB/ramdisk/goe3watt0neg" ]; then
			if [ -f "/var/www/html/openWB/ramdisk/goe3watt0pos" ]; then
				python /var/www/html/openWB/runs/simcount.py $wattc goe3 goe3poskwh goe3negkwh
			else
				#Benutze den Zählerstand aus temp_kWhCounter_lp3 als Startwert für die Simulation
				simenergy=$(echo "scale=0; $temp_kWhCounter_lp3*3600000/1" | bc)
				echo $simenergy > /var/www/html/openWB/ramdisk/goe3watt0pos
			fi
		else
			echo 0 > /var/www/html/openWB/ramdisk/goe3watt0neg
		fi
		#der ausgelesene Zählerstand wird ignoriert und stattdessen die Leistung aufintegriert
		#Grund: der ausgelesene Zählerstand hat eine Auflösung von 1kWh -> zu ungenau in der Darstellung
		if [ -f "/var/www/html/openWB/ramdisk/goe2poskwh" ]; then
			simenergy=$(echo "scale=3; $(</var/www/html/openWB/ramdisk/goe2poskwh)/1000" | bc)
			echo $simenergy > /var/www/html/openWB/ramdisk/llkwhs2
		else
			#Wenn die Simulation noch nicht gelaufen ist, nehme den Wert temp_kWhCounter_lp3
			echo $temp_kWhCounter_lp3 > /var/www/html/openWB/ramdisk/llkwhs2
		fi
	fi
	
	
	
	#car status 1 Ladestation bereit, kein Auto
	#car status 2 Auto lädt
	#car status 3 Warte auf Fahrzeug
	#car status 4 Ladung beendet, Fahrzeug verbunden
	car=$(echo $output | jq -r '.car')
	if [[ $car == "1" ]] ; then
		echo 0 > /var/www/html/openWB/ramdisk/plugstatlp3
	else
		echo 1 > /var/www/html/openWB/ramdisk/plugstatlp3
	fi
	if [[ $car == "2" ]] ; then
		echo 1 > /var/www/html/openWB/ramdisk/chargestatlp3
	else
		echo 0 > /var/www/html/openWB/ramdisk/chargestatlp3
	fi
fi
