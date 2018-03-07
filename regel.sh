#!/bin/bash
#config file einlesen
. openwb.conf


#######################################
# Werte für die Berechnung ermitteln

#Wattbezug	
if [[ $wattbezugmodul != "none" ]]; then
	wattbezug=`modules/$wattbezugmodul/main.sh`
	#uberschuss zur berechnung
	wattbezugint=`printf "%.0f\n" $wattbezug`
	uberschuss=`expr $wattbezugint \* -1`
	if [[ $debug == "1" ]]; then
		echo wattbezug $wattbezug
		echo uberschuss $uberschuss
	fi
fi

#PV Leistung ermitteln
if [[ $pvwattmodul != "none" ]]; then
	pvwatt=`modules/$pvwattmodul/main.sh`
	if [[ $debug == "1" ]]; then
                echo pvwatt $pvwatt
        fi
fi
#Ladeleistung ermitteln
if [[ $ladeleistungmodul != "none" ]]; then
	modules/$ladeleistungmodul/main.sh
	lla1=$(cat /var/www/html/openWB/ramdisk/lla1)
	lla2=$(cat /var/www/html/openWB/ramdisk/lla2)
	lla3=$(cat /var/www/html/openWB/ramdisk/lla3)	
	ladeleistung=$(cat /var/www/html/openWB/ramdisk/llaktuell)
	if [[ $debug == "1" ]]; then
                echo ladeleistung $ladeleistung
		echo lla1 $lla1
		echo lla2 $lla2
		echo lla3 $lla3
        fi
fi	

#Soc ermitteln
if [[ $socmodul != "none" ]]; then
	soc=`modules/$socmodul/main.sh`
        if [[ $debug == "1" ]]; then
                echo soc $soc
        fi
fi
#Uhrzeit
	date=$(date)
	H=$(date +%H)



#########################################
#Regelautomatiken


########################
# Sofort Laden
if grep -q 0 "/var/www/html/openWB/ramdisk/lademodus"; then
	if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
		runs/$sofortll.sh
#		runs/$ladungan.sh
		exit 0
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
		exit 0
	fi		
fi




####################
# Nachtladung bzw. Ladung bis SOC x% nachts von x bis x Uhr
if [[ $nachtladen == "1" ]]; then
	if (( $nachtladenabuhr <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H <= $nachtladenbisuhr )); then
		if [[ $socmodul != "none" ]]; then
			if (( $soc <= $nachtsoc )); then
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
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
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
					runs/ladungaus.sh
					echo "stop Nachtladung mit $nachtll um $date bei $soc" >> log/lade.log
					exit 0
				fi
				exit 0
			fi
		fi
		if [[ $socmodul == "none" ]]; then
			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
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
#Ladestromstarke berechnen
	llalt=`var/www/html/openWB/ramdisk/llsoll`
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
	if (( $anzahlphasen = 0 )); then
		anzahlphasen=1
	fi
	echo $anzahlphasen > /var/www/html/openWB/ramdisk/anzahlphasen
	else
	if [ ! -f /var/www/html/openWB/ramdisk/anzahlphasen ]; then
    		echo 1 > /var/www/html/openWB/ramdisk/anzahlphasen
	fi
	anzahlphasen=$(cat /var/www/html/openWB/ramdisk/anzahlphasen)
fi



########################
# Berechnung für PV Regelung
mindestuberschussphasen=`echo "($mindestuberschuss*$anzahlphasen)" | bc`
wattkombiniert=`echo "($ladeleistung+$uberschuss)" | bc`
abschaltungw=`echo "($abschaltuberschuss*$anzahlphasen)" | bc`
schaltschwelle=`echo "(230*$anzahlphasen)" | bc`


########################
#Min Ladung + PV Uberschussregelung lademodus 1
if grep -q 1 "/var/www/html/openWB/ramdisk/lademodus"; then
	if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
		runs/$minimalstromstaerke.sh
#		runs/ladungan.sh
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
		if (( $uberschuss < 0 )); then
                	if (( $llalt > $minimalstromstaerke )); then
                                llneu=$((llalt - 1 ))
                                runs/$llneu.sh
                                exit 0
                        else
                                exit 0
                        fi
                fi
		if (( $ubserschuss > $schaltschwelle )); then
                        if (( $llalt == $maximalstromstaerke )); then
                                exit 0
                        fi
                        llneu=$(llalt + 1 )
                        runs/$llneu.sh
                	exit 0
		fi

fi

########################
#NUR PV Uberschussregelung lademodus 2
# wenn evse aus und $mindestuberschuss vorhanden, starte evse mit 6A Ladestromstaerke (1320 - 3960 Watt je nach Anzahl Phasen)
if grep -q 2 "/var/www/html/openWB/ramdisk/lademodus"; then
	if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
			if (( $mindestuberschussphasen <= $uberschuss )); then
				runs/ladungan.sh
				runs/$minimalstromstaerke.sh
				echo "ueberschussladung $uberschuss um $date mit 6A gestartet" >> log/lade.log
				exit 0
			fi	
	fi



# wenn evse bereits an, vergleiche ladestromstaerke und uberschuss und regle nach
	if (( $wattkombiniert < $abschaltungw )); then	
		if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
			exit 0		
		fi
		if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
#minimiere Ladeleistung bis kleinste stufe erreicht, dann schalte ab
			if (( $llalt > $minimalstromstaerke )); then
				llneu=$((llalt - 1 ))
                		runs/$llneu.sh
				exit 0
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
			exit 0
		fi
		if (( $ubserschuss > $schaltschwelle )); then
			if (( $llalt == $maximalstromstaerke )); then
				exit 0
			fi
			llneu=$(llalt + 1 )
			runs/$llneu.sh
		fi
		exit 0
	fi		
fi



	







