#!/bin/bash
#set -e

#####
#
# File: set-current.sh
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
graphtimer=$(<ramdisk/graphtimer)
if (( graphtimer < 4 )); then
	graphtimer=$((graphtimer+1))
	echo $graphtimer > ramdisk/graphtimer
else
	graphtimer=0
	echo $graphtimer > ramdisk/graphtimer
	#php web/graph-l.php &
	#php web/graph-m.php &
	#php web/graph-s.php &
fi

#######################################

#Speicher werte
if [[ $speichermodul != "none" ]] ; then
	timeout 5 modules/$speichermodul/main.sh || true
fi


# Werte für die Berechnung ermitteln
llalt=$(cat /var/www/html/openWB/ramdisk/llsoll)
#PV Leistung ermitteln
if [[ $pvwattmodul != "none" ]]; then
	pvwatt=$(modules/$pvwattmodul/main.sh || true)
	if ! [[ $pvwatt =~ $re ]] ; then
		pvwatt="0"
	fi

	if [[ $debug == "1" ]]; then
                date
		echo pvwatt $pvwatt
        fi
else
	pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
fi

#Ladeleistung ermitteln
if [[ $ladeleistungmodul != "none" ]]; then
	timeout 10 modules/$ladeleistungmodul/main.sh || true
	llkwh=$(</var/www/html/openWB/ramdisk/llkwh)
	llkwhges=$llkwh
	lla1=$(cat /var/www/html/openWB/ramdisk/lla1)
	lla2=$(cat /var/www/html/openWB/ramdisk/lla2)
	lla3=$(cat /var/www/html/openWB/ramdisk/lla3)
	lla1=$(echo $lla1 | sed 's/\..*$//')
	lla2=$(echo $lla2 | sed 's/\..*$//')
	lla3=$(echo $lla3 | sed 's/\..*$//')
	ladeleistung=$(cat /var/www/html/openWB/ramdisk/llaktuell)
		if ! [[ $lla1 =~ $re ]] ; then
		 lla1="0"
	fi
	if ! [[ $lla2 =~ $re ]] ; then
		 lla2="0"
	fi

	if ! [[ $lla3 =~ $re ]] ; then
		 lla3="0"
	fi
	if ! [[ $ladeleistung =~ $re ]] ; then
		 ladeleistung="0"
	fi

else
	lla1=0
	lla2=0
	lla3=0
	ladeleistung=800
	llkwh=0
	llkwhges=$llkwh
fi
#zweiter ladepunkt
if [[ $lastmanagement == "1" ]]; then
	if [[ $socmodul1 != "none" ]]; then
		timeout 10 modules/$socmodul1/main.sh || true
		soc1=$(</var/www/html/openWB/ramdisk/soc1)
		if ! [[ $soc1 =~ $re ]] ; then
		 soc1="0"
		fi
		if [[ $debug == "1" ]]; then
	                echo soc1 $soc1
	        fi
	else
		soc1=0
	fi
	timeout 10 modules/$ladeleistungs1modul/main.sh || true
	llkwhs1=$(</var/www/html/openWB/ramdisk/llkwhs1)
	llkwhges=$(echo "$llkwhges + $llkwhs1" |bc)
	llalts1=$(cat /var/www/html/openWB/ramdisk/llsolls1)
	ladeleistungs1=$(cat /var/www/html/openWB/ramdisk/llaktuells1)
	llas11=$(cat /var/www/html/openWB/ramdisk/llas11)
	llas12=$(cat /var/www/html/openWB/ramdisk/llas12)
	llas13=$(cat /var/www/html/openWB/ramdisk/llas13)
	llas11=$(echo $llas11 | sed 's/\..*$//')
	llas12=$(echo $llas12 | sed 's/\..*$//')
	llas13=$(echo $llas13 | sed 's/\..*$//')
	if ! [[ $ladeleistungs1 =~ $re ]] ; then
	 ladeleistungs1="0"
	fi
	ladeleistung=$(( ladeleistung + ladeleistungs1 ))
	echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
else
	echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
fi
#dritter ladepunkt
if [[ $lastmanagements2 == "1" ]]; then
	timeout 10 modules/$ladeleistungs2modul/main.sh || true
	llkwhs2=$(</var/www/html/openWB/ramdisk/llkwhs2)
	llkwhges=$(echo "$llkwhges + $llkwhs2" |bc)
	llalts2=$(cat /var/www/html/openWB/ramdisk/llsolls2)
	ladeleistungs2=$(cat /var/www/html/openWB/ramdisk/llaktuells2)
	llas21=$(cat /var/www/html/openWB/ramdisk/llas21)
	llas22=$(cat /var/www/html/openWB/ramdisk/llas22)
	llas23=$(cat /var/www/html/openWB/ramdisk/llas23)
	llas21=$(echo $llas21 | sed 's/\..*$//')
	llas22=$(echo $llas22 | sed 's/\..*$//')
	llas23=$(echo $llas23 | sed 's/\..*$//')

	if ! [[ $ladeleistungs2 =~ $re ]] ; then
	 ladeleistungs2="0"
	fi
	ladeleistung=$(( ladeleistung + ladeleistungs2 ))
	echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
else
	echo "$ladeleistung" > /var/www/html/openWB/ramdisk/llkombiniert
fi
echo $llkwhges > ramdisk/llkwhges
	if [[ $debug == "1" ]]; then
                echo ladeleistung "$ladeleistung" llalt "$llalt" nachtladen "$nachtladen" minimalA "$minimalstromstaerke" maximalA "$maximalstromstaerke"
		echo lla1 "$lla1" llas11 "$llas11" llas21 "$llas21" mindestuberschuss "$mindestuberschuss" abschaltuberschuss "$abschaltuberschuss"
		echo lla2 "$lla2" llas12 "$llas12" llas22 "$llas22" sofortll "$sofortll"
		echo lla3 "$lla3" llas13 "$llas13" llas23 "$llas23"
		echo evua 1,2,3 "$evua1" "$evua2" "$evua3"
        fi
#Wattbezug
if [[ $wattbezugmodul != "none" ]]; then
	wattbezug=$(modules/$wattbezugmodul/main.sh || true)
	if ! [[ $wattbezug =~ $re ]] ; then
	wattbezug="0"
	fi
	#uberschuss zur berechnung
	wattbezugint=$(printf "%.0f\n" $wattbezug)
	uberschuss=$((wattbezugint * -1))
	if [[ $debug == "1" ]]; then
		echo wattbezug $wattbezug
		echo uberschuss $uberschuss
	fi
	evua1=$(cat /var/www/html/openWB/ramdisk/bezuga1)
	evua2=$(cat /var/www/html/openWB/ramdisk/bezuga2)
	evua3=$(cat /var/www/html/openWB/ramdisk/bezuga3)
	evua1=$(echo $evua1 | sed 's/\..*$//')
	evua2=$(echo $evua2 | sed 's/\..*$//')
	evua3=$(echo $evua3 | sed 's/\..*$//')
else
	wattbezug=$pvwatt
	wattbezugint=$(printf "%.0f\n" $wattbezug)
	wattbezugint=$(echo "($wattbezugint+$hausbezugnone+$ladeleistung)" |bc)
	echo "$wattbezugint" > /var/www/html/openWB/ramdisk/wattbezug
	uberschuss=$((wattbezugint * -1))

fi
#Soc ermitteln
if [[ $socmodul != "none" ]]; then
	timeout 10 modules/$socmodul/main.sh || true
	soc=$(</var/www/html/openWB/ramdisk/soc)
	if ! [[ $soc =~ $re ]] ; then
	 soc="0"
	fi
	if [[ $debug == "1" ]]; then
                echo soc $soc
        fi
else
	soc=0
fi
#Uhrzeit
	date=$(date)
	H=$(date +%H)

#Graphing
#Live Graphing
echo $((pvwatt * -1)) >> /var/www/html/openWB/ramdisk/pv-live.graph
echo $wattbezugint >> /var/www/html/openWB/ramdisk/evu-live.graph
echo $ladeleistung >> /var/www/html/openWB/ramdisk/ev-live.graph
echo $soc >> /var/www/html/openWB/ramdisk/soc-live.graph
date +%H:%M >> /var/www/html/openWB/ramdisk/time-live.graph
livegraph=$((livegraph * 6 ))
	if ! [[ $livegraph =~ $re ]] ; then
	 livegraph="30"
	fi
echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/pv-live.graph)" > /var/www/html/openWB/ramdisk/pv-live.graph
echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/soc-live.graph)" > /var/www/html/openWB/ramdisk/soc-live.graph
echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/evu-live.graph)" > /var/www/html/openWB/ramdisk/evu-live.graph
echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/ev-live.graph)" > /var/www/html/openWB/ramdisk/ev-live.graph 
echo "$(tail -$livegraph /var/www/html/openWB/ramdisk/time-live.graph)" > /var/www/html/openWB/ramdisk/time-live.graph
#Long Time Graphing
if (( graphtimer == 1 )) || (( graphtimer == 4 )); then
echo $((pvwatt * -1)) >> /var/www/html/openWB/ramdisk/pv.graph
echo $wattbezugint >> /var/www/html/openWB/ramdisk/evu.graph
echo $soc >> /var/www/html/openWB/ramdisk/soc.graph
echo $ladeleistung >> /var/www/html/openWB/ramdisk/ev.graph
date +%H:%M >> /var/www/html/openWB/ramdisk/time.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/pv.graph)" > /var/www/html/openWB/ramdisk/pv.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/evu.graph)" > /var/www/html/openWB/ramdisk/evu.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/soc.graph)" > /var/www/html/openWB/ramdisk/soc.graph
echo "$(tail -720 /var/www/html/openWB/ramdisk/ev.graph)" > /var/www/html/openWB/ramdisk/ev.graph 
echo "$(tail -720 /var/www/html/openWB/ramdisk/time.graph)" > /var/www/html/openWB/ramdisk/time.graph
fi
#########################################
#Regelautomatiken
########################
# Sofort Laden
if grep -q 0 "/var/www/html/openWB/ramdisk/lademodus"; then
	aktgeladen=$(<ramdisk/aktgeladen)
	#mit einem Ladepunkt
	if [[ $lastmanagement == "0" ]]; then
		if (( soc >= sofortsoclp1 )); then
			if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then

				runs/set-current.sh 0 all
				if [[ $debug == "1" ]]; then
	        		       	echo "Beende Sofort Laden da $sofortsoclp1 % erreicht"
       				fi

			fi
		exit 0
		fi
		if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
			if (( lademstat == "1" )); then
				if (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
					if [[ $debug == "1" ]]; then
	       	             			echo "Sofort ladung beendet da $lademkwh kWh lademenge erreicht"
	     				fi
				else
					runs/set-current.sh $minimalstromstaerke all
					if [[ $debug == "1" ]]; then
		        		       	echo starte sofort Ladeleistung von $minimalstromstaerke aus
        				fi
					exit 0
				fi
			else
				runs/set-current.sh $minimalstromstaerke all
				if [[ $debug == "1" ]]; then
		        	       	echo starte sofort Ladeleistung von $minimalstromstaerke aus
        			fi
				exit 0
			fi
		fi
		if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
			if (( lademstat == "1" )) && (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
				runs/set-current.sh 0 m
				if [[ $debug == "1" ]]; then
		        	       	echo "Beende Sofort Laden da  $lademkwh kWh erreicht"
        			fi

			else
				if (( evua1 < lastmaxap1 )) && (( evua2 < lastmaxap2 )) &&  (( evua3 < lastmaxap3 )); then
					if (( ladeleistung < 500 )); then
						if (( llalt > minimalstromstaerke )); then
	        	                        	llneu=$((llalt - 1 ))
	        	                        	runs/set-current.sh $llneu m
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung reudziert auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
	        	                        	exit 0
						fi
						if (( llalt == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
							exit 0
						fi
						if (( llalt < minimalstromstaerke )); then
							llneu=$((llalt + 1 ))
							runs/set-current.sh $llneu m
							if [[ $debug == "1" ]]; then
	       		             				echo "Sofort ladung erhöht auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
	     						fi
							exit 0
						fi
					else
						if (( llalt == sofortll )); then
							if [[ $debug == "1" ]]; then
	       		        	     			echo "Sofort ladung erreicht bei $sofortll A"
	     						fi
							exit 0
						fi
						if (( llalt > maximalstromstaerke )); then
							llneu=$((llalt - 1 ))
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
	       			             			echo "Sofort ladung auf $llneu reduziert, über eingestellter max A $maximalstromstaerke"
	     						fi
							exit 0
						fi
						if (( llalt < sofortll)); then
							evudiff1=$((lastmaxap1 - evua1 ))
							evudiff2=$((lastmaxap2 - evua2 ))
							evudiff3=$((lastmaxap3 - evua3 ))
							evudiffmax=($evudiff1 $evudiff2 $evudiff3)
							maxdiff=0
							for v in "${evudiffmax[@]}"; do
								if (( v > maxdiff )); then maxdiff=$v; fi;
							done
							llneu=$((llalt + maxdiff))
							if (( llneu > sofortll )); then
								llneu=$sofortll
							fi
							runs/set-current.sh "$llneu" m
			                		if [[ $debug == "1" ]]; then
	       		             				echo "Sofort ladung um $maxdiff A Differenz auf $llneu A erhoeht, kleiner als sofortll $sofortll"
	     						fi
							exit 0
						fi
						if (( llalt > sofortll)); then
							llneu=$sofortll
							runs/set-current.sh "$llneu" m
				                	if [[ $debug == "1" ]]; then
	       			             			echo "Sofort ladung von $llalt A llalt auf $llneu A reduziert, größer als sofortll $sofortll"
	     						fi
							exit 0
						fi
					fi
				else
					evudiff1=$((evua1 - lastmaxap1 ))
					evudiff2=$((evua2 - lastmaxap2 ))
					evudiff3=$((evua3 - lastmaxap3 ))
					evudiffmax=($evudiff1 $evudiff2 $evudiff3)
					maxdiff=0
					for v in "${evudiffmax[@]}"; do
						if (( v > maxdiff )); then maxdiff=$v; fi;
					done
					maxdiff=$((maxdiff + 1 ))
					llneu=$((llalt - maxdiff))
					if (( llneu < minimalstromstaerke )); then
						llneu=$minimalstromstaerke
						if [[ $debug == "1" ]]; then
							echo Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
						fi
					fi
					runs/set-current.sh "$llneu" m
	        		        if [[ $debug == "1" ]]; then
       	        		     		echo "Sofort ladung um $maxdiff auf $llneu reduziert"
     					fi
					exit 0
				fi
			fi
		fi
	else
		#mit mehr als einem ladepunkt
		aktgeladens1=$(<ramdisk/aktgeladens1)
		if (( evua1 < lastmaxap1 )) && (( evua2 < lastmaxap2 )) &&  (( evua3 < lastmaxap3 )); then
			evudiff1=$((lastmaxap1 - evua1 ))
			evudiff2=$((lastmaxap2 - evua2 ))
			evudiff3=$((lastmaxap3 - evua3 ))
			evudiffmax=($evudiff1 $evudiff2 $evudiff3)
			maxdiff=0
			for v in "${evudiffmax[@]}"; do
				if (( v > maxdiff )); then maxdiff=$v; fi;
			done
			maxdiff=$((maxdiff - 1 ))
			#Ladepunkt 1
			if (( sofortsocstatlp1 == "1" )); then
				if (( soc > sofortsoclp1 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
						runs/set-current.sh 0 m
						if [[ $debug == "1" ]]; then
			        		       	echo "Beende Sofort Laden da $sofortsoclp1 % erreicht"
       						fi
					fi
				else
					if (( ladeleistung < 500 )); then
						if (( llalt > minimalstromstaerke )); then
							llneu=$((llalt - 1 ))
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 reudziert auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalt == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalt < minimalstromstaerke )); then
							llneu=$minimalstromstaerke
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 erhöht auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
					else
						if (( llalt == sofortll )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 erreicht bei $sofortll A"
							fi
						fi
						if (( llalt > maximalstromstaerke )); then
							llneu=$((llalt - 1 ))
							runs/set-current.sh "$llneu" m
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 1 auf $llneu reduziert, über eingestellter max A $maximalstromstaerke"
							fi
						else
							if (( llalt < sofortll)); then

								llneu=$((llalt + maxdiff))
								if (( llneu > sofortll )); then
									llneu=$sofortll
								fi
								runs/set-current.sh $llneu m
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 1 um $maxdiff A Differenz auf $llneu A erhoeht, war kleiner als sofortll $sofortll"
								fi
							fi
							if (( llalt > sofortll)); then
								llneu=$sofortll
								runs/set-current.sh "$llneu" m
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 1 von $llalt A llalt auf $llneu A reduziert, war größer als sofortll $sofortll"
								fi
							fi
						fi
					fi
				fi

			else	

			if (( lademstat == "1" )) && (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
					runs/set-current.sh 0 m
					if [[ $debug == "1" ]]; then
	       				       	echo "Beende Sofort Laden an Ladepunkt 1 da  $lademkwh kWh erreicht"
       					fi
				fi
			else
				if (( ladeleistung < 500 )); then
					if (( llalt > minimalstromstaerke )); then
	                                	llneu=$((llalt - 1 ))
	                                	runs/set-current.sh "$llneu" m
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 reudziert auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
	                                fi
					if (( llalt == minimalstromstaerke )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
					if (( llalt < minimalstromstaerke )); then
						llneu=$minimalstromstaerke
						runs/set-current.sh "$llneu" m
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 erhöht auf $llneu bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
				else
					if (( llalt == sofortll )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 erreicht bei $sofortll A"
		     				fi
					fi
					if (( llalt > maximalstromstaerke )); then
						llneu=$((llalt - 1 ))
						runs/set-current.sh "$llneu" m
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 1 auf $llneu reduziert, über eingestellter max A $maximalstromstaerke"
		     				fi
					else
						if (( llalt < sofortll)); then

							llneu=$((llalt + maxdiff))
							if (( llneu > sofortll )); then
								llneu=$sofortll
							fi
							runs/set-current.sh "$llneu" m
			                		if [[ $debug == "1" ]]; then
		       	             				echo "Sofort ladung Ladepunkt 1 um $maxdiff A Differenz auf $llneu A erhoeht, war kleiner als sofortll $sofortll"
		     					fi
						fi
						if (( llalt > sofortll)); then
							llneu=$sofortll
							runs/set-current.sh "$llneu" m
			                		if [[ $debug == "1" ]]; then
		       	             				echo "Sofort ladung Ladepunkt 1 von $llalt A llalt auf $llneu A reduziert, war größer als sofortll $sofortll"
		     					fi
						fi
					fi
				fi
				
			fi
			fi
			
			#Ladepunkt 2
			if (( sofortsocstatlp2 == "1" )); then
				if (( soc1 > sofortsoclp2 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						runs/set-current.sh 0 s1
						if [[ $debug == "1" ]]; then
			        		       	echo "Beende Sofort Laden an Ladepunkt 2 da  $sofortsoclp2 % erreicht"
       						fi
					fi
				else
					if (( ladeleistungs1 < 500 )); then
						if (( llalts1 > minimalstromstaerke )); then
							llneus1=$((llalts1 - 1 ))
							runs/set-current.sh "$llneus1" s1
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 reudziert auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalts1 == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
						if (( llalts1 < minimalstromstaerke )); then
							llneus1=$minimalstromstaerke
							runs/set-current.sh "$llneus1" s1
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 erhöht auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
							fi
						fi
					else
						if (( llalts1 == sofortlls1 )); then
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 erreicht bei $sofortlls1 A"
							fi
						fi
						if (( llalts1 > maximalstromstaerke )); then
							llneus1=$((llalts1 - 1 ))
							runs/set-current.sh "$llneus1" s1
							if [[ $debug == "1" ]]; then
								echo "Sofort ladung Ladepunkt 2 auf $llneus1 reduziert, über eingestellter max A $maximalstromstaerke"
							fi
						else
							if (( llalts1 < sofortlls1)); then
								llneus1=$((llalts1 + maxdiff))
								if (( llneus1 > sofortlls1 )); then
									llneus1=$sofortlls1
								fi
								runs/set-current.sh "$llneus1" s1
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 2 um $maxdiff A Differenz auf $llneus1 A erhoeht, war kleiner als sofortll $sofortlls1"
								fi
							fi
							if (( llalts1 > sofortlls1)); then
								llneus1=$sofortlls1
								runs/set-current.sh "$llneus1" s1
								if [[ $debug == "1" ]]; then
									echo "Sofort ladung Ladepunkt 2 von $llalts1 A llalt auf $llneus1 A reduziert, war größer als sofortll $sofortlls1"
								fi
							fi
						fi
					fi
				fi
			else	
			if (( lademstats1 == "1" )) && (( $(echo "$aktgeladens1 > $lademkwhs1" |bc -l) )); then
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
					runs/set-current.sh 0 s1
					if [[ $debug == "1" ]]; then
	       				       	echo "Beende Sofort Laden an Ladepunkt 2 da  $lademkwhs1 kWh erreicht"
       					fi
				fi
			else
				if (( ladeleistungs1 < 500 )); then
					if (( llalts1 > minimalstromstaerke )); then
        	                        	llneus1=$((llalts1 - 1 ))
        	                        	runs/set-current.sh "$llneus1" s1
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 reudziert auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
        	                        fi
					if (( llalts1 == minimalstromstaerke )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
					if (( llalts1 < minimalstromstaerke )); then
						llneus1=$minimalstromstaerke
						runs/set-current.sh "$llneus1" s1
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 erhöht auf $llneus1 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
		     				fi
					fi
				else
					if (( llalts1 == sofortlls1 )); then
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 erreicht bei $sofortlls1 A"
		     				fi
					fi
					if (( llalts1 > maximalstromstaerke )); then
						llneus1=$((llalts1 - 1 ))
						runs/set-current.sh "$llneus1" s1
						if [[ $debug == "1" ]]; then
		       	             			echo "Sofort ladung Ladepunkt 2 auf $llneus1 reduziert, über eingestellter max A $maximalstromstaerke"
		     				fi
					else
						if (( llalts1 < sofortlls1)); then
							llneus1=$((llalts1 + maxdiff))
							if (( llneus1 > sofortlls1 )); then
								llneus1=$sofortlls1
							fi
							runs/set-current.sh "$llneus1" s1
			                		if [[ $debug == "1" ]]; then
		       	             				echo "Sofort ladung Ladepunkt 2 um $maxdiff A Differenz auf $llneus1 A erhoeht, war kleiner als sofortll $sofortlls1"
		     					fi
						fi
						if (( llalts1 > sofortlls1)); then
							llneus1=$sofortlls1
							runs/set-current.sh "$llneus1" s1
			                		if [[ $debug == "1" ]]; then
	       		             				echo "Sofort ladung Ladepunkt 2 von $llalts1 A llalt auf $llneus1 A reduziert, war größer als sofortll $sofortlls1"
	     						fi
						fi
					fi
				fi
			fi
			fi
			
			#Ladepunkt 3
			if [[ $lastmanagements2 == "1" ]]; then
				aktgeladens2=$(<ramdisk/aktgeladens2)
				if (( lademstats2 == "1" )) && (( $(echo "$aktgeladens2 > $lademkwhs2" |bc -l) )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
						runs/set-current.sh 0 s2
						if [[ $debug == "1" ]]; then
		       				       	echo "Beende Sofort Laden an Ladepunkt 3 da  $lademkwhs2 kWh erreicht"
       						fi
					fi
				else
					if (( ladeleistungs2 < 500 )); then
						if (( llalts2 > minimalstromstaerke )); then
			                                	llneus2=$((llalts2 - 1 ))
	                                	runs/set-current.sh "$llneus2" s2
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 reudziert auf $llneus2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
		                                fi
						if (( llalts2 == minimalstromstaerke )); then
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
						fi
						if (( llalts2 < minimalstromstaerke )); then
							llneus2=$minimalstromstaerke
							runs/set-current.sh "$llneus2" s2
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 erhöht auf $llneus2 bei minimal A $minimalstromstaerke Ladeleistung zu gering"
			     				fi
						fi
					else
						if (( llalts2 == sofortlls2 )); then
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 erreicht bei $sofortlls2 A"
			     				fi
						fi
						if (( llalts2 > maximalstromstaerke )); then
							llneus2=$((llalts2 - 1 ))
							runs/set-current.sh "$llneus2" s2
							if [[ $debug == "1" ]]; then
			       	             			echo "Sofort ladung Ladepunkt 3 auf $llneus2 reduziert, über eingestellter max A $maximalstromstaerke"
			     				fi
						else
							if (( llalts2 < sofortlls2)); then
								llneus2=$((llalts2 + maxdiff))
								if (( llneus2 > sofortlls2 )); then
									llneus2=$sofortlls2
								fi
								runs/set-current.sh "$llneus2" s2
				                		if [[ $debug == "1" ]]; then
		       		             				echo "Sofort ladung Ladepunkt 3 um $maxdiff A Differenz auf $llneus2 A erhoeht, war kleiner als sofortll $sofortlls2"
		     						fi
							fi
							if (( llalts2 > sofortlls2)); then
								llneus2=$sofortlls2
								runs/set-current.sh "$llneus2" s2
		        	        			if [[ $debug == "1" ]]; then
	       	        	     					echo "Sofort ladung Ladepunkt 3 von $llalts2 A llalt auf $llneus2 A reduziert, war größer als sofortll $sofortlls2"
	     							fi
							fi
						fi
					fi
				fi
			fi
			exit 0
			else
				evudiff1=$((evua1 - lastmaxap1 ))
				evudiff2=$((evua2 - lastmaxap2 ))
				evudiff3=$((evua3 - lastmaxap3 ))
				evudiffmax=($evudiff1 $evudiff2 $evudiff3)
				maxdiff=0
				for v in "${evudiffmax[@]}"; do
					if (( v > maxdiff )); then maxdiff=$v; fi;
				done
				maxdiff=$((maxdiff + 1 ))
				llneu=$((llalt - maxdiff))
				llneus1=$((llalts1 - maxdiff))
				if [[ $lastmanagements2 == "1" ]]; then
					llneus2=$((llalts2 - maxdiff))
				fi
				if (( llneu < minimalstromstaerke )); then
					llneu=$minimalstromstaerke
					if [[ $debug == "1" ]]; then
						echo Ladepunkt 1 Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
					fi
				fi
				if (( llneus1 < minimalstromstaerke )); then
					llneus1=$minimalstromstaerke
					if [[ $debug == "1" ]]; then
						echo Ladepunkt 2 Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
					fi
				fi
				if [[ $lastmanagements2 == "1" ]]; then
					if (( llneus2 < minimalstromstaerke )); then
						llneus2=$minimalstromstaerke
						if [[ $debug == "1" ]]; then
						echo Ladepunkt 3 Differenz groesser als minimalstromstaerke, setze auf minimal A $minimalstromstaerke
						fi
					fi
				fi
				if (( soc >= sofortsoclp1 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
						runs/set-current.sh 0 m
						if [[ $debug == "1" ]]; then
		        			       	echo "Beende Sofort Laden da $sofortsoclp1 % erreicht"
						fi
					fi
				else	
					if (( lademstat == "1" )) && (( $(echo "$aktgeladen > $lademkwh" |bc -l) )); then
						if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
							runs/set-current.sh 0 m
							if [[ $debug == "1" ]]; then
		       					       	echo "Beende Sofort Laden an Ladepunkt 1 da  $lademkwh kWh erreicht"
       							fi
						fi
					else
						runs/set-current.sh "$llneu" m
					fi
				fi
				if (( soc1 >= sofortsoclp2 )); then
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						runs/set-current.sh 0 s1
						if [[ $debug == "1" ]]; then
		        		       	echo "Beende Sofort Laden an Ladepunkt 2 da  $sofortsoclp2 % erreicht"
       						fi
					fi
				else	
					if (( lademstats1 == "1" )) && (( $(echo "$aktgeladens1 > $lademkwhs1" |bc -l) )); then
						if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
							runs/set-current.sh 0 s1
							if [[ $debug == "1" ]]; then
		       					       	echo "Beende Sofort Laden an Ladepunkt 2 da  $lademkwhs1 kWh erreicht"
       							fi
						fi
					else
						runs/set-current.sh "$llneus1" s1
					fi
				fi
				if [[ $lastmanagements2 == "1" ]]; then
					aktgeladens2=$(<ramdisk/aktgeladens2)
					if (( lademstats2 == "1" )) && (( $(echo "$aktgeladens2 > $lademkwhs2" |bc -l) )); then
						if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
							runs/set-current.sh 0 s2
							if [[ $debug == "1" ]]; then
		       					       	echo "Beende Sofort Laden an Ladepunkt 3 da  $lademkwhs2 kWh erreicht"
       							fi
						fi
					else
						runs/set-current.sh "$llneus2" s2
					fi
				fi
		        	if [[ $debug == "1" ]]; then
       		        		echo "Sofort ladung um $maxdiff auf $llneu reduziert"
     				fi
				exit 0
				
			fi
		fi
	
fi
####################
# Nachtladung bzw. Ladung bis SOC x% nachts von x bis x Uhr
if [[ $nachtladen == "1" ]]; then
	if (( nachtladenabuhr <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H <= nachtladenbisuhr )); then
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
		fi
		if [[ $socmodul == "none" ]]; then
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
		if [[ $nachtladens1 == "0" ]]; then
			exit 0
		fi
	fi
fi
#Nachtladen S1
if [[ $nachtladens1 == "1" ]]; then
	if (( nachtladenabuhrs1 <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H <= nachtladenbisuhrs1 )); then
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
		fi
		if [[ $socmodul1 == "none" ]]; then
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
	exit 0
	fi
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
if grep -q 1 "/var/www/html/openWB/ramdisk/lademodus"; then
	if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
		runs/set-current.sh $minimalampv all
		exit 0
		if [[ $debug == "1" ]]; then
   			echo "starte min + pv ladung mit $minimalampv"
   		fi
	fi
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
		if (( ladeleistung < 500 )); then
			if (( llalt == minimalampv )); then
        			exit 0
			else
				llneu=$minimalampv
			        runs/set-current.sh $llneu all 
				if [[ $debug == "1" ]]; then
      					echo "min + pv ladung auf $llneu geaendert, llalt ungleich als minimalampv, war $llalt"
        			fi
        			exit 0

			fi
		fi
		if (( uberschuss < pvregelungm )); then
  			if (( llalt > minimalampv )); then
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
					if (( llneu < minimalampv )); then
						llneu=$minimalampv
					fi
				else
					llneu=$((llalt - 1 ))
				fi
        			runs/set-current.sh $llneu all
		   		if [[ $debug == "1" ]]; then
      					echo "min + pv ladung auf $llneu reduziert"
      				fi
        			exit 0
      			else
				if (( llalt < minimalampv )); then
					llneu=$minimalampv
					runs/set-current.sh $llneu all
				fi
				exit 0
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
      			runs/set-current.sh $llneu all
			if [[ $debug == "1" ]]; then
   				echo "min + pv ladung auf $llneu erhoeht"
     			fi
    			exit 0
		fi
		exit 0
	fi
fi
########################
#NUR PV Uberschussregelung lademodus 2
# wenn evse aus und $mindestuberschuss vorhanden, starte evse mit 6A Ladestromstaerke (1320 - 3960 Watt je nach Anzahl Phasen)
if grep -q 2 "/var/www/html/openWB/ramdisk/lademodus"; then
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
#	speicherregelpunkt=$(</var/www/html/openWB/ramdisk/speicher)
#	if (( speicherregelpunkt > 10 )); then
#		runs/set-current.sh 0 all
#		exit 0
#	fi
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
fi




#Lademodus 3 == Aus

if grep -q 3 "/var/www/html/openWB/ramdisk/lademodus"; then
	if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
		runs/set-current.sh 0 all
		exit 0
	else
		exit 0
	fi
fi
