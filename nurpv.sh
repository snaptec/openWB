#!/bin/bash
#NUR PV Uberschussregelung lademodus 2
nurpvlademodus(){
. /var/www/html/openWB/openwb.conf
if [[ $lastmanagement == "0" ]]; then
	if [[ $socmodul != "none" ]]; then
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
fi
if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
	if (( ladestatuss1 == 1 )) || (( ladestatuss2 == 1 )); then
		runs/set-current.sh 0 all
	fi
	if (( mindestuberschussphasen <= uberschuss )); then
		pvecounter=$(cat /var/www/html/openWB/ramdisk/pvecounter)
		if (( pvecounter < einschaltverzoegerung )); then
			pvecounter=$((pvecounter + 10))
			echo $pvecounter > /var/www/html/openWB/ramdisk/pvecounter
			if [[ $debug == "1" ]]; then
				echo "PV Einschaltverzögerung auf $pvecounter erhöht, Ziel $einschaltverzoegerung"
			fi
			exit 0
		else
			if [[ $debug == "1" ]]; then
				echo "nur pv ladung auf $minimalapv starten"
			fi
			runs/set-current.sh $minimalapv all
			echo 0 > /var/www/html/openWB/ramdisk/pvcounter
			echo 0 > /var/www/html/openWB/ramdisk/pvecounter
			exit 0
		fi
	else
		echo 0 > /var/www/html/openWB/ramdisk/pvecounter
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
			if (( uberschuss > 2070 )); then
            	if (( anzahlphasen < 4 )); then
                	llneu=$((llalt + 2 ))
                else
            	    llneu=$((llalt + 1 ))
                fi
            fi
			if (( uberschuss > 2760 )); then
				if (( anzahlphasen < 4 )); then
					llneu=$((llalt + 2 ))
				else
					llneu=$((llalt + 1 ))
				fi
			fi
			if (( uberschuss > 3450 )); then
				if (( anzahlphasen < 4 )); then
					llneu=$((llalt + 2 ))
				else
					llneu=$((llalt + 1 ))
				fi
			fi
			if (( uberschuss > 4140 )); then
				if (( anzahlphasen < 4 )); then
					llneu=$((llalt + 2 ))
				else
					llneu=$((llalt + 1 ))
				fi
			fi
			if (( uberschuss > 4830 )); then
				if (( anzahlphasen < 4 )); then
					llneu=$((llalt + 2 ))
				else
					llneu=$((llalt + 1 ))
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
		if (( adaptpv == 1 )) && (( ladeleistung > 500 )) && (( ladeleistungs1 > 500 )) && (( soc > 0 )) && (( soc1 > 0 )) && (( anzahlphasen == 2 )); then
			socdist=$(echo $((soc1 - soc)) | sed 's/-//')
			anzahl=$((socdist / adaptfaktor))
			if (( soc1 > soc )); then
				higherev=s1
				lowerev=m
			else
				higherev=m
				lowerev=s1
			fi
			llhigher=$llneu
			lllower=$llneu
			for ((i=1;i<=anzahl;i++)); do
				if (( llhigher > minimalapv )) && (( lllower < maximalstromstaerke )); then
					llhigher=$((llhigher - 1))
					lllower=$((lllower + 1))
				fi
			done
			runs/set-current.sh $llhigher $higherev
			runs/set-current.sh $lllower $lowerev
			sleep 1
			echo $llneu > ramdisk/llsoll
			echo $llneu > ramdisk/llsolls1
			if (( debug == 1 )); then
				echo $llneu "erhoeht, adaptiert auf"
				echo auf $llhigher A für LP $higherev
				echo auf $lllower A für LP $lowerev
			fi
			
		else
			runs/set-current.sh $llneu all
			if [[ $debug == "1" ]]; then
				echo "pv ladung auf $llneu erhoeht"
			fi
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
				if (( uberschuss < -2070 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -2760 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -3450 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -4140 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -4830 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -5520 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -6210 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -6900 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
				if (( uberschuss < -7590 )); then
					if (( anzahlphasen < 4 )); then
						llneu=$((llalt - 3 ))
					else
						llneu=$((llalt - 1 ))
					fi
				fi
			else
				llneu=$((llalt - 1 ))
			fi
			if (( llneu < minimalapv )); then
				llneu=$minimalapv
			fi
			echo $llneu
			if (( adaptpv == 1 )) && (( ladeleistung > 500 )) && (( ladeleistungs1 > 500 )) && (( soc > 0 )) && (( soc1 > 0 )) && (( anzahlphasen == 2 )); then
				socdist=$(echo $((soc1 - soc)) | sed 's/-//')
				anzahl=$((socdist / adaptfaktor))
				if (( soc1 > soc )); then
					higherev=s1
					lowerev=m
				else
					higherev=m
					lowerev=s1
				fi
				llhigher=$llneu
				lllower=$llneu
				for ((i=1;i<=anzahl;i++)); do
					if (( llhigher > minimalapv )) && (( lllower < maximalstromstaerke )); then
						llhigher=$((llhigher - 1))
						lllower=$((lllower + 1))
					fi
				done
				runs/set-current.sh $llhigher $higherev
				runs/set-current.sh $lllower $lowerev
				sleep 1
				echo $llneu > ramdisk/llsoll
				echo $llneu > ramdisk/llsolls1

				if (( debug == 1 )); then
					echo $llneu "reduziert, adaptiert auf"
					echo auf $llhigher A für LP $higherev
					echo auf $lllower A für LP $lowerev
				fi
			else

				runs/set-current.sh $llneu all
				if [[ $debug == "1" ]]; then
					echo "pv ladung auf $llneu reduziert"
				fi
			fi
			echo 0 > /var/www/html/openWB/ramdisk/pvcounter
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

