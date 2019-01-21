#!/bin/bash
#NUR PV Uberschussregelung lademodus 2
nurpvlademodus(){
# wenn evse aus und $mindestuberschuss vorhanden, starte evse mit 6A Ladestromstaerke (1320 - 3960 Watt je nach Anzahl Phasen)
#	if (( ladeleistung > 500 )); then
#		if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
#			runs/set-current.sh 0 m
#     			exit 0
#		fi
#		if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
#			runs/set-current.sh 0 s1
#     			exit 0
#		fi
#		if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
#			runs/set-current.sh 0 s2
#     			exit 0
#		fi
#	fi
if [[ $lastmanagement == "0" ]]; then
	if (( soc < minnurpvsoclp1 )); then
		if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
			runs/set-current.sh $minnurpvsocll all 
			if [[ $debug == "1" ]]; then
				echo "Starte PV Laden da $sofortsoclp1 % zu gering"
			fi

		fi
	exit 0
	fi
	if (( soc > maxnurpvsoclp1 )); then
		if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
			runs/set-current.sh 0 all
			if [[ $debug == "1" ]]; then
				echo "Beende PV Laden da $sofortsoclp1 % erreicht"
			fi
		fi
	exit 0
	fi
fi
if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
	if (( ladestatuss1 == 1 )) || (( ladestatuss2 == 1 )); then
		runs/set-current.sh 0 all
	fi
	if (( mindestuberschussphasen <= uberschuss )); then
		if [[ $debug == "1" ]]; then
   			echo "nur  pv ladung auf $minimalapv starten"
  		fi
		runs/set-current.sh $minimalapv all
		echo 0 > /var/www/html/openWB/ramdisk/pvcounter
		exit 0
	else
		exit 0
	fi
fi
if (( ladeleistung < 500 )); then
	if (( llalt > minimalapv )); then
		llneu=$minimalapv
		runs/set-current.sh $llneu all
		echo 0 > /var/www/html/openWB/ramdisk/pvcounter
		exit 0
	fi
	if (( llalt < minimalapv )); then
		llneu=$minimalapv
		runs/set-current.sh $llneu all
		echo 0 > /var/www/html/openWB/ramdisk/pvcounter
		exit 0
	fi
	if (( llalt == minimalapv )); then
		if (( wattbezugint > abschaltuberschuss )); then
			pvcounter=$(cat /var/www/html/openWB/ramdisk/pvcounter)
			if (( pvcounter < abschaltverzoegerung )); then
				pvcounter=$((pvcounter + 10))
				echo $pvcounter > /var/www/html/openWB/ramdisk/pvcounter
				if [[ $debug == "1" ]]; then
					echo "Nur PV auf Minimalstromstaerke, PV Counter auf $pvcounter erhöht"
				fi
			else
				runs/set-current.sh 0 all
				if [[ $debug == "1" ]]; then
					echo "pv ladung beendet"
				fi
			fi
		fi
	fi
else
	if [[ $speichervorhanden == "1" ]]; then
		if (( speicherleistung < 0 )); then
			uberschuss=$((uberschuss + speicherleistung))
			wattbezugint=$((wattbezugint - speicherleistung))
		fi
	fi
	if (( uberschuss > schaltschwelle )); then
		if (( llalt == maximalstromstaerke )); then
			exit 0
		fi
		if (( uberschuss > 1380 )); then
			if (( anzahlphasen < 4 )); then
				llneu=$((llalt + 5 ))
			else
				llneu=$((llalt + 2 ))
			fi
			if (( uberschuss > 2760 )); then
				if (( anzahlphasen < 4 )); then
					llneu=$((llalt + 11 ))
				else
					llneu=$((llalt + 3 ))
				fi
			fi
			if (( llneu > maximalstromstaerke )); then
				llneu=$maximalstromstaerke
			fi
		else
			llneu=$((llalt + 1 ))
		fi
		if (( llalt < minimalapv )); then
			llneu=$minimalapv
		fi
		runs/set-current.sh $llneu all
		if [[ $debug == "1" ]]; then
			echo "pv ladung auf $llneu erhoeht"
		fi
		echo 0 > /var/www/html/openWB/ramdisk/pvcounter
		exit 0
	fi
	if (( uberschuss < pvregelungm )); then
		if (( llalt > minimalapv )); then
			if (( uberschuss < -1380 )); then
				if (( anzahlphasen < 4 )); then
					llneu=$((llalt - 6 ))
				else
					llneu=$((llalt - 2 ))
				fi
				if (( uberschuss < -2760 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 12 ))
					else
						llneu=$((llalt - 4 ))
					fi
				fi
				if (( llneu < minimalapv )); then
					llneu=$minimalapv
				fi
			else
				llneu=$((llalt - 1 ))
			fi
			runs/set-current.sh $llneu all
			echo 0 > /var/www/html/openWB/ramdisk/pvcounter
			if [[ $debug == "1" ]]; then
				echo "pv ladung auf $llneu reduziert"
			fi
			exit 0
		else
			if (( wattbezugint > abschaltuberschuss )); then
				pvcounter=$(cat /var/www/html/openWB/ramdisk/pvcounter)
				if (( pvcounter < abschaltverzoegerung )); then
					pvcounter=$((pvcounter + 10))
					echo $pvcounter > /var/www/html/openWB/ramdisk/pvcounter
					if [[ $debug == "1" ]]; then
						echo "Nur PV auf Minimalstromstaerke, PV Counter auf $pvcounter erhöht"
					fi
				else
					runs/set-current.sh 0 all
					if [[ $debug == "1" ]]; then
						echo "pv ladung beendet"
					fi
					echo 0 > /var/www/html/openWB/ramdisk/pvcounter
				fi
				exit 0
			else
				echo 0 > /var/www/html/openWB/ramdisk/pvcounter
				exit 0
			fi
		fi
	fi
fi


}

