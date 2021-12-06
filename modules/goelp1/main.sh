#!/bin/bash
re='^-?[0-9]+$'
rekwh='^[-+]?[0-9]+\.?[0-9]*$'


python /var/www/html/openWB/modules/goelp1/restzeit.py

output=$(curl --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/status)
if [[ $? == "0" ]] ; then
	goecorrectionfactor=$(echo "scale=0;$goecorrectionfactorlp1 * 100000 /1" |bc)
    echo $goecorrectionfactor > /var/www/html/openWB/ramdisk/goecorrectionlp1
	watt=$(echo $output | jq -r '.nrg[11]')
	watt=$(echo "scale=0;$watt * 10 /1" |bc)
	if [[ $watt =~ $re ]] ; then
        if [[ $goesimulationlp1 == "0" ]] ; then
            echo $watt > /var/www/html/openWB/ramdisk/llaktuell
        else
		    wattc=$((watt*$goecorrectionfactor/100000))
		    wattc=$(echo "scale=0;$wattc" |bc)
		    echo $wattc > /var/www/html/openWB/ramdisk/llaktuell
        fi
	fi
	lla1=$(echo $output | jq -r '.nrg[4]')
	lla1=$(echo "scale=1;$lla1 / 10" |bc)
	if [[ $lla1 =~ $rekwh ]] ; then
		echo $lla1 > /var/www/html/openWB/ramdisk/lla1
	fi
	lla2=$(echo $output | jq -r '.nrg[5]')
	lla2=$(echo "scale=1;$lla2 / 10" |bc)
	if [[ $lla2 =~ $rekwh ]] ; then		
        echo $lla2 > /var/www/html/openWB/ramdisk/lla2
	fi
	lla3=$(echo $output | jq -r '.nrg[6]')
	lla3=$(echo "scale=1;$lla3 / 10" |bc)
	if [[ $lla3 =~ $rekwh ]] ; then
		echo $lla3 > /var/www/html/openWB/ramdisk/lla3
	fi
	llv1=$(echo $output | jq -r '.nrg[0]')
	if [[ $llv1 =~ $re ]] ; then
		echo $llv1 > /var/www/html/openWB/ramdisk/llv1
	fi
	llv2=$(echo $output | jq -r '.nrg[1]')
	if [[ $llv2 =~ $re ]] ; then
		echo $llv2 > /var/www/html/openWB/ramdisk/llv2
	fi
	llv3=$(echo $output | jq -r '.nrg[2]')
	if [[ $llv3 =~ $re ]] ; then
		echo $llv3 > /var/www/html/openWB/ramdisk/llv3
	fi
	llkwh=$(echo $output | jq -r '.eto')
	llkwh=$(echo "scale=3;$llkwh / 10" |bc)
	rfid=$(echo $output | jq -r '.uby')
	oldrfid=$(</var/www/html/openWB/ramdisk/tmpgoelp1rfid)
	if [[ $rfid != $oldrfid ]] ; then
		echo $rfid > /var/www/html/openWB/ramdisk/readtag
		echo $rfid > /var/www/html/openWB/ramdisk/tmpgoelp1rfid
	fi
	if [[ $goesimulationlp1 == "0" ]] ; then
		if [[ $llkwh =~ $rekwh ]] ; then
			echo $llkwh > /var/www/html/openWB/ramdisk/llkwh
		fi
	else	
		temp_kWhCounter_lp1=$(</var/www/html/openWB/ramdisk/temp_kWhCounter_lp1)
		#simulation der Energiemenge während des ladens
		#wenn die Dateien noch nicht da sind, werden sie angelegt. Simulation startet im nächsten Regelschritt.
		if [ -f "/var/www/html/openWB/ramdisk/goewatt0neg" ]; then
			if [ -f "/var/www/html/openWB/ramdisk/goewatt0pos" ]; then
				python /var/www/html/openWB/runs/simcount.py $wattc goe goeposkwh goenegkwh
			else
				#Benutze den Zählerstand aus temp_kWhCounter_lp1 als Startwert für die Simulation
				simenergy=$(echo "scale=0; $temp_kWhCounter_lp1*3600000/1" | bc)
				echo $simenergy > /var/www/html/openWB/ramdisk/goewatt0pos
			fi
		else
			echo 0 > /var/www/html/openWB/ramdisk/goewatt0neg
		fi
		#der ausgelesene Zählerstand wird ignoriert und stattdessen die Leistung aufintegriert
		#Grund: der ausgelesene Zählerstand hat eine Auflösung von 1kWh -> zu ungenau in der Darstellung
		if [ -f "/var/www/html/openWB/ramdisk/goeposkwh" ]; then
			simenergy=$(echo "scale=3; $(</var/www/html/openWB/ramdisk/goeposkwh)/1000" | bc)
			echo $simenergy > /var/www/html/openWB/ramdisk/llkwh
		else
			#Wenn die Simulation noch nicht gelaufen ist, nehme den Wert temp_kWhCounter_lp1
			echo $temp_kWhCounter_lp1 > /var/www/html/openWB/ramdisk/llkwh
		fi
	fi
	#car status 1 Ladestation bereit, kein Auto
	#car status 2 Auto lädt
	#car status 3 Warte auf Fahrzeug
	#car status 4 Ladung beendet, Fahrzeug verbunden
	# ladestatuslp1=$(</var/www/html/openWB/ramdisk/ladestatus)
	plugstat=$(</var/www/html/openWB/ramdisk/plugstat)
	car=$(echo $output | jq -r '.car')
	# openwbDebugLog "Debug" 0 "$lp1name: pushbplug: $pushbplug  | car: $car | pushbenachrichtigung: $pushbenachrichtigung | plugstat: $plugstat"
	if [[ $plugstat == "0" ]] ; then
		if [[ $pushbplug == "1" ]] && [[ $car != "1" ]] && [[ $pushbenachrichtigung == "1" ]] ; then
			message="$lp1name eingesteckt. Ladung startet bei erfüllter Ladebedingung automatisch."
			/var/www/html/openWB/runs/pushover.sh "$message"
		fi
	fi
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
    lastseen=$(date +"%d.%m.%Y %H:%M:%S")
	echo $lastseen >/var/www/html/openWB/ramdisk/goelp1lastcontact
    mosquitto_pub -t openWB/lp/1/lastSeen -r -m "$lastseen"
	
	goelp1estimatetime=$(</var/www/html/openWB/ramdisk/goelp1estimatetime)
	mosquitto_pub -t openWB/lp/1/goeestimatetime -r -m "$goelp1estimatetime"
fi
