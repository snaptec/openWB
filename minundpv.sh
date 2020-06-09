#!/bin/bash
########################
#Min Ladung + PV Uberschussregelung lademodus 1
minundpvlademodus(){
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
	fi
	if (( speichersoc >= speichersochystminpv )); then
		if (( ladestatus == 0 )); then
			if (( speichersoc >= speichersocminpv )); then
				runs/set-current.sh $minimalampv all
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

