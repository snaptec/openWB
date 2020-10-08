#!/bin/bash
#NUR PV Uberschussregelung lademodus 2
nurpvlademodus(){
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
			if (( schieflastmax < maximalstromstaerke )); then
				maximalstromstaerke=$schieflastmaxa
				echo "$date Maximalstromstärke begrenzt auf $schieflastmaxa da Schieflastbegrenzung konfiguriert" >> ramdisk/nurpv.log
			fi
		fi
	fi
fi
if (( stopchargeafterdisclp1 == 0 )); then
	if [[ $stopchargepvatpercentlp1 == "1" ]]; then
		if (( soc > stopchargepvpercentagelp1 )); then
			if [[ $lp1enabled == "1" ]]; then
				mosquitto_pub -r -t "openWB/set/lp/1/ChargePointEnabled" -m "0"
				echo "$date LP1, Lademodus NurPV. Schalte Ladepunkt auf gesperrt da $soc % SoC erreicht, Ziel $stopchargepvpercentagelp1 %" >> ramdisk/ladestatus.log
				echo "$date LP1, Lademodus NurPV. Schalte Ladepunkt auf gesperrt da $soc % SoC erreicht, Ziel $stopchargepvpercentagelp1 %" >> ramdisk/nurpv.log
				echo "SoC PV Begrenzung (Limit: $stopchargepvpercentagelp1%) LP1 aktiv, LP gesperrt" > ramdisk/lastregelungaktiv

			fi
		fi
		if (( soc < stopchargepvpercentagelp1 )); then
			if [[ $lp1enabled == "0" ]]; then
				mosquitto_pub -r -t "openWB/set/lp/1/ChargePointEnabled" -m "1"
				echo "$date LP1, Lademodus NurPV. Schalte Ladepunkt frei da $soc % SoC noch nicht erreicht, Ziel $stopchargepvpercentagelp1 %" >> ramdisk/ladestatus.log
				echo "$date LP1, Lademodus NurPV. Schalte Ladepunkt frei da $soc % SoC noch nicht erreicht, Ziel $stopchargepvpercentagelp1 %" >> ramdisk/nurpv.log
				echo "SoC PV Begrenzung LP1 (Limit: $stopchargepvpercentagelp1%) unterschritten, LP entsperrt" > ramdisk/lastregelungaktiv

			fi
		fi
	fi
fi
if (( stopchargeafterdisclp2 == 0 )); then
	if [[ $stopchargepvatpercentlp2 == "1" ]]; then
		if (( soc1 > stopchargepvpercentagelp2 )); then
			if [[ $lp2enabled == "1" ]]; then
				mosquitto_pub -r -t "openWB/set/lp/2/ChargePointEnabled" -m "0"
				echo "$date LP2, Lademodus NurPV. Schalte Ladepunkt auf gesperrt da $soc1 % SoC erreicht, Ziel $stopchargepvpercentagelp2 %" >> ramdisk/ladestatus.log
				echo "$date LP2, Lademodus NurPV. Schalte Ladepunkt auf gesperrt da $soc1 % SoC erreicht, Ziel $stopchargepvpercentagelp2 %" >> ramdisk/nurpv.log
				echo "SoC PV Begrenzung LP2 (Limit: $stopchargepvpercentagelp2%) aktiv, LP gesperrt" > ramdisk/lastregelungaktiv

			fi
		fi
		if (( soc1 < stopchargepvpercentagelp2 )); then
			if [[ $lp2enabled == "0" ]]; then
				mosquitto_pub -r -t "openWB/set/lp/2/ChargePointEnabled" -m "1"
				echo "$date LP2, Lademodus NurPV. Schalte Ladepunkt frei da $soc % SoC noch nicht erreicht, Ziel $stopchargepvpercentagelp2 %" >> ramdisk/ladestatus.log
				echo "$date LP2, Lademodus NurPV. Schalte Ladepunkt frei da $soc % SoC noch nicht erreicht, Ziel $stopchargepvpercentagelp2 %" >> ramdisk/nurpv.log
				echo "SoC PV Begrenzung LP2 (Limit: $stopchargepvpercentagelp2%) unterschritten, LP entsperrt" > ramdisk/lastregelungaktiv

			fi
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
			echo "Ladung mit $minnurpvsocll Ampere, da $soc % SoC noch nicht erreicht" > ramdisk/lastregelungaktiv
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
	if [[ $debug == "1" ]]; then
		echo "Überschuss $uberschuss; mindestens $mindestuberschussphasen"
	fi
	if (( mindestuberschussphasen <= uberschuss )); then
		echo "$date Uberschuss $uberschuss ist größer als nötiger Überschuss, Wert: $mindestuberschussphasen" >> ramdisk/nurpv.log
		pvecounter=$(cat /var/www/html/openWB/ramdisk/pvecounter)
		if (( pvecounter < einschaltverzoegerung )); then
			echo "$date Einschaltverzögerung aktiv, Aktuell: $pvecounter, Ziel: $einschaltverzoegerung" >> ramdisk/nurpv.log
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
			echo "$date Einschaltverzögerung erreicht, Aktuell: $pvecounter, Ziel: $einschaltverzoegerung" >> ramdisk/nurpv.log
			if (( minimalapv == minimalalp2pv )); then
				runs/set-current.sh $minimalapv all
				echo "$date starte Ladung" >> ramdisk/nurpv.log
				echo "$date alle Ladepunkte, Lademodus NurPV. Ladung gestartet mit $minimalapv Ampere" >> ramdisk/ladestatus.log
			else
				echo "$date starte Ladung LP1 mit $minimalapv" >> ramdisk/nurpv.log
				runs/set-current.sh $minimalapv m
				echo "$date LP1, Lademodus NurPV. Ladung gestartet mit $minimalapv Ampere" >> ramdisk/ladestatus.log
				echo "$date starte Ladung LP2 mit $minimalalp2pv" >> ramdisk/nurpv.log
				runs/set-current.sh $minimalalp2pv s1
				echo "$date LP2, Lademodus NurPV. Ladung gestartet mit $minimalalp2pv Ampere" >> ramdisk/ladestatus.log
			fi
			echo 0 > /var/www/html/openWB/ramdisk/pvcounter
			echo 0 > /var/www/html/openWB/ramdisk/pvecounter
			echo "$date setzte Soctimer hoch zum Abfragen des aktuellen SoC" >> ramdisk/nurpv.log
			echo 20000 > /var/www/html/openWB/ramdisk/soctimer
			exit 0
		fi
	else
		echo 0 > /var/www/html/openWB/ramdisk/pvecounter
		exit 0
	fi
fi

if (( ladeleistung < 300 )); then
	echo "$date Keine Ladung aktiv" >> ramdisk/nurpv.log
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
				echo "$date Ladefreigabe aufgehoben da zu wenig Uberschuss vorhanden" >> ramdisk/nurpv.log
			#fi
		fi
	fi
else
	if [[ $speichervorhanden == "1" ]]; then
		if (( speicherleistung < 10 )); then
			if (( speichersoc > speichersocnurpv )); then
				uberschuss=$((uberschuss + speicherleistung + speicherwattnurpv))
				echo "$date SpeicherSoc ($speichersoc) über konfiguriertem Wert ($speichersocnurpv), neuer Überschusswert: $uberschuss" >> ramdisk/nurpv.log
			else
				uberschuss=$((uberschuss + speicherleistung))
				echo "$date SpeicherSoc ($speichersoc) unter konfiguriertem Wert ($speichersocnurpv), neuer Überschusswert: $uberschuss" >> ramdisk/nurpv.log
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
		echo "$date Uberschuss ($uberschuss) ist größer als Schaltschwelle ($schaltschwelle), neuer Ladestromwert: $llneu" >> ramdisk/nurpv.log
		if (( adaptpv == 1 )) && (( soc > 0 )) && (( soc1 > 0 )) && (( (( anzahlphasen == 6 )) || (( anzahlphasen == 2 )) )); then
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
			if (( adaptpv == 1 )) && (( soc > 0 )) && (( soc1 > 0 )) && (( (( anzahlphasen == 6 )) || (( anzahlphasen == 2 )) )); then
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
			echo "$date Uberschuss ($uberschuss) geringer als herunterschaltschwelle ($pvregelungm), neuer Ladestromwert: $llneu" >> ramdisk/nurpv.log
			echo 0 > /var/www/html/openWB/ramdisk/pvcounter
			exit 0
		else
			if [[ $nurpv70dynact == "1" ]]; then
				nurpv70status=$(<ramdisk/nurpv70dynstatus)
				if [[ $nurpv70status == "1" ]]; then
					abschaltuberschuss=$(( 1500 * anzahlphasen ))
					if [[ $debug == "1" ]]; then
						echo "Setze neue Abschwaltschwelle"
					fi
				fi
			fi
			if [[ $debug == "1" ]]; then
				echo Abschaltschwelle: $((-abschaltuberschuss)), Überschuss derzeit: $uberschuss
			fi
			
			if (( uberschuss < -abschaltuberschuss )); then
				pvcounter=$(cat /var/www/html/openWB/ramdisk/pvcounter)
				if (( pvcounter < abschaltverzoegerung )); then
					pvcounter=$((pvcounter + 10))
					echo $pvcounter > /var/www/html/openWB/ramdisk/pvcounter
					if [[ $debug == "1" ]]; then
						echo "Nur PV auf Minimalstromstaerke, PV Counter auf $pvcounter erhöht"
					fi
					echo "$date Uberschuss ($uberschuss) kleiner als Abschwaltschwelle ($abschaltuberschuss), Verzögerung ($pvcounter) kleiner als Ziel $abschaltverzoegerung Sec" >> ramdisk/nurpv.log
				else
					echo "$date Abschaltverzögerung erreicht, stoppe Ladung" >> ramdisk/nurpv.log
					runs/set-current.sh 0 all
					echo "$date alle Ladepunkte, Lademodus NurPV. Ladung gestoppt zu wenig PV Leistung: $uberschuss" >>  ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "pv ladung beendet"
					fi
					echo 0 > /var/www/html/openWB/ramdisk/pvcounter
				fi
				exit 0
			else
				echo "$date Minimalstromstärke erreicht, Überschuss größer als Abschaltschwelle" >> ramdisk/nurpv.log
				echo 0 > /var/www/html/openWB/ramdisk/pvcounter
				exit 0
			fi
		fi
	fi
fi


}

