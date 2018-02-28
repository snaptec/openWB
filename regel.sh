#!/bin/bash
#config file einlesen
. openwb.conf


#######################################
# Werte für die Berechnung ermitteln

#Wattbezug	
	wattbezug=`modules/$wattbezugmodul/main.sh`
	#uberschuss zur berechnung
	wattbezugint=`printf "%.0f\n" $wattbezug`
	uberschuss=`expr $wattbezugint \* -1`
	if [[ $debug == "1" ]]; then
		echo wattbezug $wattbezug
		echo uberschuss $uberschuss
	fi

#PV Leistung ermitteln
	pvwatt=`modules/$pvwattmodul/main.sh`
	if [[ $debug == "1" ]]; then
                echo pvwatt $pvwatt
        fi

#Ladeleistung ermitteln
	modules/$ladeleistung/main.sh
	lla1=$(cat /var/run/lla1)
	lla2=$(cat /var/run/lla2)
	lla3=$(cat /var/run/lla3)	
	ladeleistung=$(cat /var/run/llaktuell)
	if [[ $debug == "1" ]]; then
                echo ladeleistung $ladeleistung
		echo lla1 $lla1
		echo lla2 $lla2
		echo lla3 $lla3
        fi
	
#Soc ermitteln
	soc=`modules/$socmodul/main.sh`
        if [[ $debug == "1" ]]; then
                echo soc $soc
        fi

#Uhrzeit
	date=$(date)
	H=$(date +%H)



#########################################
#Regelautomatiken

#Prüfen ob Automatikmodus aktiv ist
	if grep -q 0 "/var/run/automatik"; then
		exit 0
	fi


####################
# Nachtladung bzw. Ladung bis SOC x% nachts von x bis x Uhr
if [[ $nachtladen == "1" ]]; then
	if (( $nachtladenabuhr <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H <= $nachtladenbisuhr )); then
		if [[ $socmodul != "none" ]]; then
			if (( $soc <= $nachtsoc )); then
				if grep -q 0 "/var/run/ladestatus"; then
					runs/ladungan.sh
					runs/$nachtll.sh
					if [[ $debug == "1" ]]; then
		                		echo "soc $soc"
		        			echo "ladeleistung" $nachtll
					fi
					echo "start Nachtladung mit $nachtll um $date bei $soc" >> log/lade.log
					exit 0
				fi
				exit 0
			else
				if grep -q 1 "/var/run/ladestatus"; then
					runs/ladungaus.sh
					echo "stop Nachtladung mit $nachtll um $date bei $soc" >> log/lade.log
					exit 0
				fi
				exit 0
			fi
		fi
		if [[ $socmodul == "none" ]]; then
			if grep -q 0 "/var/run/ladestatus"; then
				runs/ladungan.sh
                                runs/$nachtll.sh
                                if [[ $debug == "1" ]]; then
                                	echo "soc $soc"
                                        echo "ladeleistung" $nachtll
                                fi
                                echo "start Nachtladung mit $nachtll um $date" >> log/lade.log
                                exit 0
			fi
		exit 0
		fi	
	fi
fi

#######################
#Ladeleistung berechnen
	llalt=`var/run/llsoll`
	llphasentest=`expr $llalt - "3"`

#Anzahl genutzter Phasen ermitteln, wenn ladestrom kleiner 3 (nicht vorhanden) nutze den letzten bekannten wert
if (( $llalt > 3 )); then
	anzahlphasen=0
	if [ $lla1 -ge $llphasentest ]; then
		anzahlphasen=$((anzahlphasen + 1 ))
	fi
	if [ $lla2 -ge $llphasentest ]; then
	        anzahlphasen=$((anzahlphasen + 1 ))
	fi
	if [ $lla3 -ge $llphasentest ]; then
	        anzahlphasen=$((anzahlphasen + 1 ))
	fi
	echo $anzahlphasen > /var/run/anzahlphasen
	else
	if [ ! -f /var/run/anzahlphasen ]; then
    		echo 1 > /var/run/anzahlphasen
	fi
	anzahlphasen=$(cat /var/run/anzahlphasen)
fi


########################
#PV Uberschussregelung
# wenn evse aus und $mindestuberschuss vorhanden, starte evse mit 6A Ladeleistung (1320 - 3960 Watt je nach Anzahl Phasen)

	if grep -q 0 "/var/run/ladestatus"; then
		mindestuberschussphasen=`echo "($mindestuberschuss*$anzahlphasen)" | bc`
			if (( $mindestuberschussphasen <= $uberschuss )); then
				runs/ladungan.sh
				runs/ll6.sh
				echo "ueberschussladung $uberschuss um $date mit 6A gestartet" >> log/lade.log
				exit 0
			fi	
	fi



# wenn evse bereits an, vergleiche ladeleistung und uberschuss und regle nach
wattkombiniert=`echo "($ladeleistung+$uberschuss)" | bc`
abschaltungw=`echo "($abschaltuberschuss*$anzahlphasen)" | bc`
schaltschwelle=`echo "(230*$anzahlphasen)" | bc`

if (( $wattkombiniert < $abschaltungw )); then	
	if grep -q 0 "/var/run/ladestatus"; then
			exit 0		
	fi
	if grep -q 1 "/var/run/ladestatus"; then
#minimiere Ladeleistung bis kleinste stufe erreicht, dann schalte ab
		if (( $llalt > $minimalladeleistung )); then
			llneu=$((llalt - 1 ))
                	runs/$llneu.sh
		else
			runs/ladungaus.sh
			echo "uberschussladung bei uberschuss $uberschuss und wattkombiniert $wattkombiniert um $date beendet"  >> log/lade.log
			exit 0
		fi
	fi
	else
	
	if (( $uberschuss < 0 )); then
		llneu=$((llalt - 1 ))
		runs/$llneu.sh
	fi
	if (( $ubserschuss > $schaltschwelle )); then
		if (( $llalt == $maximalladeleistung )); then
			exit 0
		fi
		llneu=$(llalt + 1 ))
		runs/$llneu.sh
	fi
	exit 0
	
fi		




	







