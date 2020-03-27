#!/bin/bash
#NUR PV Uberschussregelung lademodus 2
nurpvlademodus(){
. /var/www/html/openWB/openwb.conf
maxll=($llalt $llalts1 $llalts2 $llaltlp4 $llaltlp5 $llaltlp6 $llaltlp7 $llaltlp8)
maxllvar=0
for v in "${maxll[@]}"; do
	if (( v > maxllvar )); then maxllvar=$v; fi;
done
llalt=$maxllvar
if (( llalt > minimalapv )); then
	if (( llaltlp1 == minimalapv )); then
		llalt=$minimalapv
	fi
fi

if [[ $schieflastaktiv == "1" ]]; then
	if [[ $u1p3paktiv == "1" ]]; then
		u1p3pstat=$(<ramdisk/u1p3pstat)
		if [[ $u1p3pstat == "1" ]]; then
			maximalstromstaerke=$schieflastmaxa
		fi
	fi
fi
if [[ $lastmanagement == "0" ]]; then
	if [[ $socmodul != "none" ]]; then
		if (( soc < minnurpvsoclp1 )); then
			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
				runs/set-current.sh $minnurpvsocll all
				echo "$date LP1, Lademodus NurPV. Ladung mit $minnurpvsocll Ampere, $soc % SoC noch nicht erreicht" >> ramdisk/ladestatus.log

				if [[ $debug == "1" ]]; then
					echo "Starte PV Laden da $sofortsoclp1 % zu gering"
				fi
			else
				if (( llalt != minnurpvsocll )); then
					runs/set-current.sh $minnurpvsocll all
					echo "$date LP1, Lademodus NurPV. Ladung geändert auf $minnurpvsocll Ampere, $soc % SoC noch nicht erreicht" >> ramdisk/ladestatus.log
				fi
			fi 
		exit 0
		fi
		if (( soc > maxnurpvsoclp1 )); then
			if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
				runs/set-current.sh 0 all
				echo "$date LP1, Lademodus NurPV. Ladung gestoppt, $soc % SoC erreicht" >> ramdisk/ladestatus.log
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
		echo "$date alle Ladepunkte, Lademodus NurPV. Ladung gestoppt" >> ramdisk/ladestatus.log
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
			if (( minimalapv == minimalalp2pv )); then
				runs/set-current.sh $minimalapv all
				echo "$date alle Ladepunkte, Lademodus NurPV. Ladung gestartet mit $minimalapv Ampere" >> ramdisk/ladestatus.log
			else
				runs/set-current.sh $minimalapv m
				echo "$date LP1, Lademodus NurPV. Ladung gestartet mit $minimalapv Ampere" >> ramdisk/ladestatus.log
				runs/set-current.sh $minimalalp2pv s1
				echo "$date LP2, Lademodus NurPV. Ladung gestartet mit $minimalalp2pv Ampere" >> ramdisk/ladestatus.log
			fi
			echo 0 > /var/www/html/openWB/ramdisk/pvcounter
			echo 0 > /var/www/html/openWB/ramdisk/pvecounter
			echo 20000 > /var/www/html/openWB/ramdisk/soctimer
			exit 0
		fi
	else
		echo 0 > /var/www/html/openWB/ramdisk/pvecounter
		exit 0
	fi
fi

if (( ladeleistung < 300 )); then
	if (( llalt > minimalapv )); then
		llneu=$minimalapv
		if (( minimalapv == minimalalp2pv )); then
			runs/set-current.sh $llneu all
			echo "$date alle Ladepunkte, Lademodus NurPV. Ladung geändert auf $llneu Ampere" >> ramdisk/ladestatus.log

		else
			runs/set-current.sh $minimalapv m
			echo "$date LP1, Lademodus NurPV. Ladung geändert auf $minimalapv Ampere" >> ramdisk/ladestatus.log
			runs/set-current.sh $minimalalp2pv s1
			echo "$date LP2, Lademodus NurPV. Ladung geändert auf $minimalalp2pv Ampere" >> ramdisk/ladestatus.log
		fi
		echo 0 > /var/www/html/openWB/ramdisk/pvcounter
		exit 0
	fi
	if (( llalt < minimalapv )); then
		llneu=$minimalapv
		if (( minimalapv == minimalalp2pv )); then
			runs/set-current.sh $llneu all
			echo "$date alle Ladepunkte, Lademodus NurPV. Ladung geändert auf $llneu Ampere" >> ramdisk/ladestatus.log
		else
			runs/set-current.sh $minimalapv m
			echo "$date LP1, Lademodus NurPV. Ladung geändert auf $minimalapv Ampere" >> ramdisk/ladestatus.log
			runs/set-current.sh $minimalalp2pv s1
			echo "$date LP2, Lademodus NurPV. Ladung geändert auf $minimalalp2pv Ampere" >> ramdisk/ladestatus.log
		fi
		echo 0 > /var/www/html/openWB/ramdisk/pvcounter
		exit 0
	fi
	if (( llalt == minimalapv )); then
		if (( uberschuss < mindestuberschussphasen )); then
		#if (( wattbezugint > abschaltuberschuss )); then
			#pvcounter=$(cat /var/www/html/openWB/ramdisk/pvcounter)
			#if (( pvcounter < abschaltverzoegerung )); then
			#	pvcounter=$((pvcounter + 10))
			#	echo $pvcounter > /var/www/html/openWB/ramdisk/pvcounter
			#	if [[ $debug == "1" ]]; then
			#		echo "Nur PV auf Minimalstromstaerke, PV Counter auf $pvcounter erhöht"
			#	fi
			#else
				if [ -e ramdisk/nurpvoff ]; then
					runs/set-current.sh 0 all
					echo "$date alle Ladepunkte, Lademodus NurPV. Ladefreigabe aufgehoben, Überschuss unterschritten" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "pv ladung beendet"
					fi
					rm ramdisk/nurpvoff
				else
					touch ramdisk/nurpvoff
				fi
			#fi
		fi
	fi
else
	if [[ $speichervorhanden == "1" ]]; then
		if (( speicherleistung < 0 )); then
			if (( speichersoc > speichersocnurpv )); then
				uberschuss=$((uberschuss + speicherleistung + speicherwattnurpv))
				wattbezugint=$((wattbezugint - speicherleistung - speicherwattnurpv))

			else
				uberschuss=$((uberschuss + speicherleistung))
				wattbezugint=$((wattbezugint - speicherleistung))
			fi
		fi
	fi
	if (( uberschuss > schaltschwelle )); then
		if (( llalt == maximalstromstaerke )); then
			if [[ $debug == "1" ]]; then
				echo "llalt == maximalstromstaerke"
			fi
			#exit 0
		fi
		if [[ $pvbezugeinspeisung == "0" ]]; then
			if (( nurpvslowup == 1 )); then
				llneu=$(( llalt + 1 ))
			else
				llneu=$(( llalt + ( uberschuss / 230 / anzahlphasen)))
			fi
		else
			if (( llalt == minimalapv )); then
				llneu=$(( llalt + 1 ))
			else
				if (( nurpvslowup == 1 )); then
					llneu=$(( llalt + 1 ))
				else
					llneu=$(( llalt + ( (uberschuss - schaltschwelle) / 230 / anzahlphasen)))
				fi
			fi
		fi
		if (( llneu > maximalstromstaerke )); then
			llneu=$maximalstromstaerke
		fi
		if (( llneu < minimalapv )); then
			llneu=$minimalapv
		fi
		if (( adaptpv == 1 )) && (( soc > 0 )) && (( soc1 > 0 )) && (( anzahlphasen == 2 )); then
			if (( minimalalp2pv > minimalapv )); then
				minimalapv=$minimalalp2pv
			fi
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
			echo "$date LP$higherev, Lademodus NurPV. Adaptive PV Ladung geändert auf $llhigher Ampere" >> ramdisk/ladestatus.log
			runs/set-current.sh $lllower $lowerev
			echo "$date LP$lowerev, Lademodus NurPV. Adaptive PV Ladung geändert auf $lllower Ampere" >>  ramdisk/ladestatus.log
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
			echo "$date alle Ladepunkte, Lademodus NurPV. Ladung geändert auf $llneu Ampere" >>  ramdisk/ladestatus.log
			if [[ $debug == "1" ]]; then
				echo "pv ladung auf $llneu erhoeht"
			fi
		fi
		echo 0 > /var/www/html/openWB/ramdisk/pvcounter
		exit 0
	fi
	if (( uberschuss < pvregelungm )); then
		if (( llalt > minimalapv )); then

			llneu=$(( llalt - 1 + ( (uberschuss - pvregelungm) / 230 / anzahlphasen)))
			if (( llneu < minimalapv )); then
				llneu=$minimalapv
			fi
			if (( adaptpv == 1 )) && (( soc > 0 )) && (( soc1 > 0 )) && ((anzahlphasen == 2 )); then
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
				echo "$date LP$higherev, Lademodus NurPV. Adaptive PV Ladung geändert auf $llhigher Ampere" >>  ramdisk/ladestatus.log
				runs/set-current.sh $lllower $lowerev
				echo "$date LP$lowerev, Lademodus NurPV. Adaptive PV Ladung geändert auf $lllower Ampere" >>  ramdisk/ladestatus.log

				sleep 1
				echo $llneu > ramdisk/llsoll
				echo $llneu > ramdisk/llsolls1

				if (( debug == 1 )); then
					echo $llneu "reduziert, adaptiert auf"
					echo auf $llhigher A für LP $higherev
					echo auf $lllower A für LP $lowerev
				fi
			else
				if (( minimalapv == minimalalp2pv )); then
					runs/set-current.sh $llneu all

					echo "$date alle Ladepunkte, Lademodus NurPV. Ladung geändert auf $llneu Ampere" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "pv ladung auf $llneu reduziert"
					fi
				else
					runs/set-current.sh $llneu m

					echo "$date LP1, Lademodus NurPV. Ladung geändert auf $llneu Ampere" >> ramdisk/ladestatus.log
					if (( llneu < minimalalp2pv )); then
						llneulp2=$minimalalp2pv
					else
						llneulp2=$llneu
					fi		
					runs/set-current.sh $llneulp2 s1
					echo "$date LP2, Lademodus NurPV. Ladung geändert auf $llneulp2 Ampere" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "pv ladung auf $llneu bzw. $llneulp2 reduziert"
					fi
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
					echo "$date alle Ladepunkte, Lademodus NurPV. Ladung gestoppt zu wenig PV Leistung" >>  ramdisk/ladestatus.log
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

