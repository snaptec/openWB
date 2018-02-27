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



# Nachtladung bzw. Ladung bis SOC x% nachts von x bis x Uhr
if [[ $nachtladen == "1" ]]; then
	if (( $nachtladenabuhr <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H <= $nachtladenbisuhr )); then
		if [[ $socmodul != "none" ]]; then
			if (( $soc <= $nachtsoc )); then
				if grep -q 0 "/var/run/ladestatus"; then
					runs/ladungan.sh
					runs/$nachtll
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
                                runs/$nachtll
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







