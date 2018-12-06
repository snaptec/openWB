#!/bin/bash
#set -e

#####
#
# File: regel.sh
#
# Copyright 2018 Kevin Wieland, David Meder-Marouelli
#
#  This file is part of openWB.
#
#     openWB is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     openWB is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with openWB.  If not, see <https://www.gnu.org/licenses/>.
#
#####

set -o pipefail
cd /var/www/html/openWB/
#config file einlesen
. openwb.conf
source minundpv.sh
source nurpv.sh
source auslademodus.sh
source sofortlademodus.sh
source goecheck.sh
source loadvars.sh
source graphing.sh

re='^-?[0-9]+$'
#ladelog ausfuehren
./ladelog.sh &
#doppelte Ausfuehrungsgeschwindigkeit
if [[ $dspeed == "1" ]]; then
	if [ -e ramdisk/5sec ]; then
		sleep 5 && ./regel.sh >> /var/log/openWB.log 2>&1 &
		rm ramdisk/5sec
	else
		touch ramdisk/5sec
	fi
fi
if [[ $dspeed == "2" ]]; then

	if [ -e ramdisk/5sec ]; then
		rm ramdisk/5sec
		exit 0
	else
		touch ramdisk/5sec
	fi
fi

graphtimer=$(<ramdisk/graphtimer)
if (( graphtimer < 4 )); then
	graphtimer=$((graphtimer+1))
	echo $graphtimer > ramdisk/graphtimer
else
	graphtimer=0
	echo $graphtimer > ramdisk/graphtimer
fi

#######################################
#goe mobility check
goecheck
#load charging vars
loadvars

#Graphing
graphing
#########################################
#Regelautomatiken

####################
# Nachtladung bzw. Ladung bis SOC x% nachts von x bis x Uhr
if [[ $nachtladen == "1" ]]; then
	if (( nachtladenabuhr <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H < nachtladenbisuhr )); then
		nachtladenstate=1
		dayoftheweek=$(date +%w)
		if [ "$dayoftheweek" -ge 0 ] && [ "$dayoftheweek" -le 4 ]; then
			diesersoc=$nachtsoc
		else
			diesersoc=$nachtsoc1
		fi
		if [[ $socmodul != "none" ]]; then
			if [[ $debug == "1" ]]; then
                		echo nachtladen mit socmodul $socmodul
    			fi
			if (( soc <= diesersoc )); then
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					runs/set-current.sh "$nachtll" m
					if [[ $debug == "1" ]]; then
		   				echo "soc $soc"
		      				echo "ladeleistung nachtladen bei $nachtll"
					fi
				fi
				if ! grep -q $nachtll "/var/www/html/openWB/ramdisk/llsoll"; then
					runs/set-current.sh "$nachtll" m
					if [[ $debug == "1" ]]; then
		      				echo aendere nacht Ladeleistung auf $nachtll
		        		fi
				fi
			else
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
					runs/set-current.sh 0 m
				fi
			fi
		else
			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
 				runs/set-current.sh "$nachtll" m
 				if [[ $debug == "1" ]]; then
      					echo "soc $soc"
        				echo "ladeleistung nachtladen $nachtll A"
        			fi
			else
				if ! grep -q $nachtll "/var/www/html/openWB/ramdisk/llsoll"; then
					runs/set-current.sh "$nachtll" m
					if [[ $debug == "1" ]]; then
      						echo aendere nacht Ladeleistung auf $nachtll
        				fi
				fi
			fi
		fi
	else
		nachtladenstate=0
	fi
else
	nachtladenstate=0
fi
#Nachtladen S1
if [[ $nachtladens1 == "1" ]]; then
	if (( nachtladenabuhrs1 <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H < nachtladenbisuhrs1 )); then
		nachtladenstates1=1
		dayoftheweek=$(date +%w)
		if [ "$dayoftheweek" -ge 0 ] && [ "$dayoftheweek" -le 4 ]; then
			diesersocs1=$nachtsocs1
		else
			diesersocs1=$nachtsoc1s1
		fi
		if [[ $socmodul1 != "none" ]]; then
			if [[ $debug == "1" ]]; then
                		echo nachtladen mit socmodul $socmodul1
    			fi
			if (( soc1 <= diesersocs1 )); then
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
					runs/set-current.sh "$nachtlls1" s1
					if [[ $debug == "1" ]]; then
		   				echo "soc $soc1"
		      				echo "ladeleistung nachtladen bei $nachtlls1"
					fi
				fi
				if ! grep -q $nachtlls1 "/var/www/html/openWB/ramdisk/llsolls1"; then
					runs/set-current.sh "$nachtlls1" s1
					if [[ $debug == "1" ]]; then
	      					echo aendere nacht Ladeleistung auf $nachtlls1
	        			fi
				fi
			else
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
					runs/set-current.sh 0 s1
				fi
			fi
		else
			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
 				runs/set-current.sh "$nachtlls1" s1
 				if [[ $debug == "1" ]]; then
      					echo "soc $soc1"
        				echo "ladeleistung nachtladen $nachtlls1 A"
        			fi
        			echo "start Nachtladung mit $nachtlls1 um $date" >> web/lade.log
			else
				if ! grep -q $nachtlls1 "/var/www/html/openWB/ramdisk/llsolls1"; then
					runs/set-current.sh "$nachtlls1" s1
					if [[ $debug == "1" ]]; then
	      					echo aendere nacht Ladeleistung auf $nachtlls1
	        			fi
				fi

			fi
		fi
	else
		nachtladenstates1=0
	fi
else
	nachtladenstates1=0
fi
echo $nachtladenstate > /var/www/html/openWB/ramdisk/nachtladenstate
echo $nachtladenstates1 > /var/www/html/openWB/ramdisk/nachtladenstates1

if (( nachtladenstate == 1 )) || (( nachtladenstates1 == 1 )); then
	exit 0
fi

########################
# Sofort Laden
if (( lademodus == 0 )); then
	sofortlademodus	
fi

#######################
#Ladestromstarke berechnen
llphasentest=$((llalt - 3))
#Anzahl genutzter Phasen ermitteln, wenn ladestrom kleiner 3 (nicht vorhanden) nutze den letzten bekannten wert
if (( llalt > 3 )); then
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
	echo $anzahlphasen > /var/www/html/openWB/ramdisk/anzahlphasen
else
	if [ ! -f /var/www/html/openWB/ramdisk/anzahlphasen ]; then
  	echo 1 > /var/www/html/openWB/ramdisk/anzahlphasen
	fi
	anzahlphasen=$(cat ramdisk/anzahlphasen)
fi
if (( lastmanagement == 1 )); then
	if (( llas11 > 3 )); then
		if [ "$llas11" -ge $llphasentest ]; then
			anzahlphasen=$((anzahlphasen + 1 ))
		fi
		if [ "$llas12" -ge $llphasentest ]; then
	  	anzahlphasen=$((anzahlphasen + 1 ))
		fi
		if [ "$llas13" -ge $llphasentest ]; then
			anzahlphasen=$((anzahlphasen + 1 ))
		fi

		echo $anzahlphasen > /var/www/html/openWB/ramdisk/anzahlphasen
	fi
fi
if (( lastmanagements2 == 1 )); then
	if (( llas21 > 3 )); then
		if [ "$llas21" -ge $llphasentest ]; then
			anzahlphasen=$((anzahlphasen + 1 ))
		fi
		if [ "$llas22" -ge $llphasentest ]; then
	  	anzahlphasen=$((anzahlphasen + 1 ))
		fi
		if [ "$llas23" -ge $llphasentest ]; then
			anzahlphasen=$((anzahlphasen + 1 ))
		fi
		echo $anzahlphasen > /var/www/html/openWB/ramdisk/anzahlphasen
	fi
fi
if [ $anzahlphasen -eq 0 ]; then
	anzahlphasen=1
fi
########################
# Berechnung für PV Regelung
mindestuberschussphasen=$(echo "($mindestuberschuss*$anzahlphasen)" | bc)
wattkombiniert=$(echo "($ladeleistung+$uberschuss)" | bc)
abschaltungw=$(echo "(($abschaltuberschuss-1320)*-1*$anzahlphasen)" | bc)
schaltschwelle=$(echo "(230*$anzahlphasen)" | bc)
if [[ $debug == "2" ]]; then
	ladestatus=$(cat ramdisk/ladestatus)
	echo "$date"
	echo uberschuss "$uberschuss"
	echo wattbezug "$wattbezug"
	echo ladestatus "$ladestatus"
	echo llsoll "$llalt"
	echo pvwatt "$pvwatt"
	echo mindestuberschussphasen "$mindestuberschussphasen"
	echo wattkombiniert "$wattkombiniert"
	echo abschaltungw "$abschaltungw"
	echo schaltschwelle "$schaltschwelle"
fi
#PV Regelmodus
if [[ $pvbezugeinspeisung == "0" ]]; then
	pvregelungm="0"
fi
if [[ $pvbezugeinspeisung == "1" ]]; then
	pvregelungm=$(echo "(230*$anzahlphasen*-1)" | bc)
	schaltschwelle="0"
fi

########################
#Min Ladung + PV Uberschussregelung lademodus 1
if (( lademodus == 1 )); then
	minundpvlademodus
fi
########################
#NUR PV Uberschussregelung lademodus 2
# wenn evse aus und $mindestuberschuss vorhanden, starte evse mit 6A Ladestromstaerke (1320 - 3960 Watt je nach Anzahl Phasen)
if (( lademodus == 2 )); then
	nurpvlademodus
fi



#Lademodus 3 == Aus

if (( lademodus == 3 )); then
	auslademodus
fi
