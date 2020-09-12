#!/bin/bash
########################
#Min Ladung + PV Uberschussregelung lademodus 1
minundpvlademodus(){


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
	maxll=($llalt $llalts1 $llalts2 $llaltlp4 $llaltlp5 $llaltlp6 $llaltlp7 $llaltlp8)
	maxllvar=0
	for v in "${maxll[@]}"; do
		if (( v > maxllvar )); then maxllvar=$v; fi;
	done
	llalt=$maxllvar
	if [[ $schieflastaktiv == "1" ]]; then
		if [[ $u1p3paktiv == "1" ]]; then
			u1p3pstat=$(<ramdisk/u1p3pstat)
			if [[ $u1p3pstat == "1" ]]; then
				maximalstromstaerke=$schieflastmaxa
			fi
		fi
	fi
	if [[ $speichervorhanden == "1" ]]; then 
		if (( speicherleistung < 0 )); then 
			uberschuss=$((uberschuss + speicherleistung)) 
		fi 
	else
		speichersoc=0
		speichersochystminpv=0
		speichersocminpv=0
	fi
	if (( speichersoc >= speichersochystminpv )); then
		if (( ladestatus == 0 )); then
			if (( speichersoc >= speichersocminpv )); then
				runs/set-current.sh $minimalampv all
				echo "$date setzte Soctimer hoch zum Abfragen des aktuellen SoC" >> ramdisk/nurpv.log
				echo 20000 > /var/www/html/openWB/ramdisk/soctimer
				echo "$date alle Ladepunkte, Lademodus Min und PV. Starte Ladung mit $minimalampv Ampere" >> ramdisk/ladestatus.log
				if [[ $debug == "1" ]]; then
					echo "starte min + pv ladung mit $minimalampv"
				fi
			fi
		else
			if (( ladeleistung < 500 )); then
				llneu=$minimalampv
				#runs/set-current.sh $llneu all 
			else
				if (( uberschuss < pvregelungm )); then
					if (( llalt > minimalampv )); then
						#llneu=$(( llalt + ( uberschuss / 230 / anzahlphasen)))
						llneu=$(( llalt - 1 + ( (uberschuss - pvregelungm) / 230 / anzahlphasen)))


						#runs/set-current.sh $llneu all
					else
						llneu=$minimalampv
						#runs/set-current.sh $llneu all
					fi
				else
					llneu=$llalt
				fi
				if (( uberschuss > schaltschwelle )); then
					if [[ $pvbezugeinspeisung == "0" ]]; then
						llneu=$(( llalt + ( uberschuss / 230 / anzahlphasen)))

					else
						if (( llalt == minimalampv )); then
							llneu=$(( llalt + 1 ))
						else
							llneu=$(( llalt + ( (uberschuss - schaltschwelle) / 230 / anzahlphasen)))
						fi
					fi
					if (( llneu > maximalstromstaerke )); then
						llneu=$maximalstromstaerke
					fi
					if (( llalt < minimalampv )); then
						llneu=$minimalampv
					fi
				fi
			fi
			if (( llneu < minimalampv )); then
				llneu=$minimalampv

			fi
			if (( llneu > maximalstromstaerke )); then
				llneu=$maximalstromstaerke
			fi
			runs/set-current.sh $llneu all
			if (( llalt != llneu )); then
				echo "$date alle Ladepunkte, Lademodus Min und PV. Ändere Ladeleistung auf $llneu Ampere" >> ramdisk/ladestatus.log
			fi
		fi
	else
		runs/set-current.sh 0 all
	fi

}

