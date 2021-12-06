#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'

python /var/www/html/openWB/modules/goelp2/restzeit.py

output=$(curl --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/status)
if [[ $? == "0" ]] ; then
	goecorrectionfactor=$(echo "scale=0;$goecorrectionfactorlp2 * 100000 /1" |bc)
	echo $goecorrectionfactor > /var/www/html/openWB/ramdisk/goecorrectionlp2
	watt=$(echo $output | jq -r '.nrg[11]')
	watt=$(echo "scale=0;$watt * 10 /1" |bc)
	if [[ $watt =~ $re ]] ; then
		if [[ $goesimulationlp1 == "0" ]] ; then
			echo $watt > /var/www/html/openWB/ramdisk/llaktuells1
		else
			wattc=$((watt*$goecorrectionfactor/100000))
			wattc=$(echo "scale=0;$wattc" |bc)
			echo $wattc > /var/www/html/openWB/ramdisk/llaktuells1
		fi
	fi
	lla1=$(echo $output | jq -r '.nrg[4]')
	lla1=$(echo "scale=1;$lla1 / 10" |bc)
	if [[ $lla1 =~ $rekwh ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/llas11
	fi
	lla2=$(echo $output | jq -r '.nrg[5]')
	lla2=$(echo "scale=1;$lla2 / 10" |bc)
	if [[ $lla2 =~ $rekwh ]] ; then
		echo $lla2 > /var/www/html/openWB/ramdisk/llas12
	fi
	lla3=$(echo $output | jq -r '.nrg[6]')
	lla3=$(echo "scale=1;$lla3 / 10" |bc)
	if [[ $lla3 =~ $rekwh ]] ; then
		echo $lla3 > /var/www/html/openWB/ramdisk/llas13
	fi
	llv1=$(echo $output | jq -r '.nrg[0]')
	if [[ $llv1 =~ $re ]] ; then
		echo $llv1 > /var/www/html/openWB/ramdisk/llvs11
	fi
	llv2=$(echo $output | jq -r '.nrg[1]')
	if [[ $llv2 =~ $re ]] ; then
		echo $llv2 > /var/www/html/openWB/ramdisk/llvs12
	fi
	llv3=$(echo $output | jq -r '.nrg[2]')
	if [[ $llv3 =~ $re ]] ; then
		echo $llv3 > /var/www/html/openWB/ramdisk/llvs13
	fi
	llkwh=$(echo $output | jq -r '.eto')
	llkwh=$(echo "scale=3;$llkwh / 10" |bc)	
	rfid=$(echo $output | jq -r '.uby')
	oldrfid=$(</var/www/html/openWB/ramdisk/tmpgoelp2rfid)
	if [[ $rfid != $oldrfid ]] ; then
		echo $rfid > /var/www/html/openWB/ramdisk/readtag
		echo $rfid > /var/www/html/openWB/ramdisk/tmpgoelp2rfid
	fi
	if [[ $goesimulationlp2 == "0" ]] ; then
		if [[ $llkwh =~ $rekwh ]] ; then
			echo $llkwh > /var/www/html/openWB/ramdisk/llkwhs1
		fi
	else	
		temp_kWhCounter_lp2=$(</var/www/html/openWB/ramdisk/temp_kWhCounter_lp2)
		#simulation der Energiemenge während des ladens
		#wenn die Dateien noch nicht da sind, werden sie angelegt. Simulation startet im nächsten Regelschritt.
		if [ -f "/var/www/html/openWB/ramdisk/goe2watt0neg" ]; then
			if [ -f "/var/www/html/openWB/ramdisk/goe2watt0pos" ]; then
				python /var/www/html/openWB/runs/simcount.py $wattc goe2 goe2poskwh goe2negkwh
			else
				#Benutze den Zählerstand aus temp_kWhCounter_lp2 als Startwert für die Simulation
				simenergy=$(echo "scale=0; $temp_kWhCounter_lp2*3600000/1" | bc)
				echo $simenergy > /var/www/html/openWB/ramdisk/goe2watt0pos
			fi
		else
			echo 0 > /var/www/html/openWB/ramdisk/goe2watt0neg
		fi
		#der ausgelesene Zählerstand wird ignoriert und stattdessen die Leistung aufintegriert
		#Grund: der ausgelesene Zählerstand hat eine Auflösung von 1kWh -> zu ungenau in der Darstellung
		if [ -f "/var/www/html/openWB/ramdisk/goe2poskwh" ]; then
			simenergy=$(echo "scale=3; $(</var/www/html/openWB/ramdisk/goe2poskwh)/1000" | bc)
			echo $simenergy > /var/www/html/openWB/ramdisk/llkwhs1
		else
			#Wenn die Simulation noch nicht gelaufen ist, nehme den Wert temp_kWhCounter_lp2
			echo $temp_kWhCounter_lp2 > /var/www/html/openWB/ramdisk/llkwhs1
		fi
	fi
	#car status 1 Ladestation bereit, kein Auto
	#car status 2 Auto lädt
	#car status 3 Warte auf Fahrzeug
	#car status 4 Ladung beendet, Fahrzeug verbunden
	plugstat=$(</var/www/html/openWB/ramdisk/plugstats1)
	car=$(echo $output | jq -r '.car')
	# openwbDebugLog "Debug" 0 "$lp2name: pushbplug: $pushbplug  | car: $car | pushbenachrichtigung: $pushbenachrichtigung | plugstat: $plugstat"
	if [[ $plugstat == "0" ]] ; then
		if [[ $pushbplug == "1" ]] && [[ $car != "1" ]] && [[ $pushbenachrichtigung == "1" ]] ; then
			message="$lp2name eingesteckt. Ladung startet bei erfüllter Ladebedingung automatisch."
			/var/www/html/openWB/runs/pushover.sh "$message"
		fi
	fi
	if [[ $car == "1" ]] ; then
		echo 0 > /var/www/html/openWB/ramdisk/plugstats1
	else
		echo 1 > /var/www/html/openWB/ramdisk/plugstats1
	fi
	if [[ $car == "2" ]] ; then
		echo 1 > /var/www/html/openWB/ramdisk/chargestats1
	else
		echo 0 > /var/www/html/openWB/ramdisk/chargestats1
	fi
	lastseen=$(date +"%d.%m.%Y %H:%M:%S")
	echo $lastseen >/var/www/html/openWB/ramdisk/goelp2lastcontact
    mosquitto_pub -t openWB/lp/2/lastSeen -r -m "$lastseen"
	
	goelp2estimatetime=$(</var/www/html/openWB/ramdisk/goelp2estimatetime)
	mosquitto_pub -t openWB/lp/2/goeestimatetime -r -m "$goelp2estimatetime"
fi