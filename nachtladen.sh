#!/bin/bash
lastmnacht() {
	if [[ $schieflastaktiv == "1" ]]; then
		if [[ $u1p3paktiv == "1" ]]; then
			u1p3pstat=$(<ramdisk/u1p3pstat)
			if [[ $u1p3pstat == "1" ]]; then
				maximalstromstaerke=$schieflastmaxa
			fi
		fi
	fi
	if [ $# -eq 2 ]; then
		if ((evua1 < lastmaxap1)) && ((evua2 < lastmaxap2)) && ((evua3 < lastmaxap3)); then
			evudiff1=$((lastmaxap1 - evua1))
			evudiff2=$((lastmaxap2 - evua2))
			evudiff3=$((lastmaxap3 - evua3))
			evudiffmax=("$evudiff1" "$evudiff2" "$evudiff3")
			maxdiff=${evudiffmax[0]}
			for v in "${evudiffmax[@]}"; do
				if ((v < maxdiff)); then maxdiff=$v; fi
			done
			if (($1 == $2)); then
				llnachtreturn=$2
			else
				if (($2 == 0)); then
					llnachtreturn=$2
				else
					if (($1 > $2)); then
						llnachtreturn=$(($1 - 1))
					else
						if ((maxdiff > 1)); then
							llnachtreturn=$(($1 + 1))
						else
							llnachtreturn=$1
						fi
					fi
					if ((llnachtreturn > maximalstromstaerke)); then
						llnachtreturn=$2
					fi
					if ((llnachtreturn < minimalstromstaerke)); then
						llnachtreturn=$minimalstromstaerke
					fi
				fi
			fi
		else
			evudiff1=$((evua1 - lastmaxap1))
			evudiff2=$((evua2 - lastmaxap2))
			evudiff3=$((evua3 - lastmaxap3))
			evudiffmax=("$evudiff1" "$evudiff2" "$evudiff3")
			maxdiff=0
			for vv in "${evudiffmax[@]}"; do
				if ((vv > maxdiff)); then maxdiff=$vv; fi
			done
			maxdiff=$((maxdiff + 1))
			llnachtreturn=$(($1 - maxdiff))
			if ((llnachtreturn < minimalstromstaerke)); then
				llnachtreturn=$minimalstromstaerke
				openwbDebugLog "MAIN" 1 "Differenz groesser als minimalstromstaerke, setze Nachtladen auf minimal A $minimalstromstaerke"
			fi
			echo "Lastmanagement aktiv, Ladeleistung reduziert" >ramdisk/lastregelungaktiv
			openwbDebugLog "MAIN" 1 "Nachtladen um $maxdiff auf $llnachtreturn reduziert"
		fi
	fi
}

nachtlademodus() {
	if [[ $nachtladen == "1" ]]; then
		if ((nachtladenabuhr <= 10#$H && 10#$H <= 24)) || ((0 <= 10#$H && 10#$H < nachtladenbisuhr)); then
			nachtladenstate=1
			dayoftheweek=$(date +%w)
			currenthour=$(date +%k)
			if [[ $dayoftheweek -eq 0 && $currenthour -ge 14 ]] || [[ $dayoftheweek -ge 1 && $dayoftheweek -le 4 ]] || [[ $dayoftheweek -eq 5 && $currenthour -le 11 ]]; then
				diesersoc=$nachtsoc
			else
				diesersoc=$nachtsoc1
			fi
			if [[ $socmodul != "none" ]]; then
				openwbDebugLog "MAIN" 1 "nachtladen mit socmodul $socmodul"
				if ((soc <= diesersoc)); then
					if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
						llnachtneu=$nachtll
						#runs/set-current.sh "$nachtll" m
						openwbDebugLog "MAIN" 1 "soc $soc Ladeleistung Nachtladen bei $nachtll"
					fi
					if ! grep -q "$nachtll" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$nachtll
						#runs/set-current.sh "$nachtll" m
						openwbDebugLog "MAIN" 1 "aendere Nacht-Ladeleistung auf $nachtll"
					fi
				else
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
						llnachtneu=0
						#runs/set-current.sh 0 m
					fi
				fi
			else
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$nachtll
					#runs/set-current.sh "$nachtll" m
					openwbDebugLog "MAIN" 1 "Ladeleistung Nachtladen $nachtll A"
				else
					if ! grep -q "$nachtll" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$nachtll
						#runs/set-current.sh "$nachtll" m
						openwbDebugLog "MAIN" 1 "aendere Nacht-Ladeleistung auf $nachtll"
					fi
				fi
			fi
			if [ -z "$llnachtneu" ]; then
				llnachtneu=$llalt
			fi
		else
			nachtladenstate=0
		fi
		#Morgens Laden LP1
		dayoftheweek=$(date +%w)
		currenttime=$(date +%H:%M)
		#Sonntag
		if ((dayoftheweek == 0)); then
			if [[ "$currenttime" > "$mollp1soab" ]] && [[ "$currenttime" < "$mollp1sobis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1soll
					openwbDebugLog "CHARGESTAT" 0 "Sonntag morgens Laden gestartet mit $mollp1soll A"
					openwbDebugLog "MAIN" 1 "Ladeleistung Sonntag morgens Laden $mollp1soll A"
				else
					if ! grep -q "$mollp1soll" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1soll
						openwbDebugLog "MAIN" 1 "aendere Ladeleistung Sonntag morgens Laden $mollp1soll A"
					fi
				fi
				if [ -z "$llnachtneu" ]; then
					llnachtneu=$llalt
				fi
			else
				nachtladen2state=0
			fi
		fi

		#Montag
		if ((dayoftheweek == 1)); then
			if [[ "$currenttime" > "$mollp1moab" ]] && [[ "$currenttime" < "$mollp1mobis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1moll
					openwbDebugLog "CHARGESTAT" 0 "Montag morgens Laden gestartet mit $mollp1moll A"
					openwbDebugLog "MAIN" 1 "Ladeleistung Sonntag morgens Laden $mollp1moll A"
				else
					if ! grep -q "$mollp1moll" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1moll
						openwbDebugLog "MAIN" 1 "aendere Ladeleistung Montag morgens Laden $mollp1moll A"
					fi
				fi
				if [ -z "$llnachtneu" ]; then
					llnachtneu=$llalt
				fi
			else
				nachtladen2state=0
			fi
		fi

		#Dienstag
		if ((dayoftheweek == 2)); then
			if [[ "$currenttime" > "$mollp1diab" ]] && [[ "$currenttime" < "$mollp1dibis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1dill
					openwbDebugLog "CHARGESTAT" 0 "Dienstag morgens Laden gestartet mit $mollp1dill A"
					openwbDebugLog "MAIN" 1 "Ladeleistung Dienstag morgens Laden $mollp1dill A"
				else
					if ! grep -q "$mollp1dill" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1dill
						openwbDebugLog "MAIN" 1 "aendere Ladeleistung Dienstag morgens Laden $mollp1dill A"
					fi
				fi
				if [ -z "$llnachtneu" ]; then
					llnachtneu=$llalt
				fi
			else
				nachtladen2state=0
			fi
		fi

		#Mittwoch
		if ((dayoftheweek == 3)); then
			if [[ "$currenttime" > "$mollp1miab" ]] && [[ "$currenttime" < "$mollp1mibis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1mill
					openwbDebugLog "CHARGESTAT" 0 "Mittwoch morgens Laden gestartet mit $mollp1mill A"
					openwbDebugLog "MAIN" 1 "Ladeleistung Mittwoch morgens Laden $mollp1mill A"
				else
					if ! grep -q "$mollp1mill" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1mill
						openwbDebugLog "MAIN" 1 "aendere Ladeleistung Mittwoch morgens Laden $mollp1mill A"
					fi
				fi
				if [ -z "$llnachtneu" ]; then
					llnachtneu=$llalt
				fi
			else
				nachtladen2state=0
			fi
		fi

		#Donnerstag
		if ((dayoftheweek == 4)); then
			if [[ "$currenttime" > "$mollp1doab" ]] && [[ "$currenttime" < "$mollp1dobis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1doll
					openwbDebugLog "CHARGESTAT" 0 "Donnerstag morgens Laden gestartet mit $mollp1doll A"
					openwbDebugLog "MAIN" 1 "Ladeleistung Donnerstag morgens Laden $mollp1doll A"
				else
					if ! grep -q "$mollp1doll" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1doll
						openwbDebugLog "MAIN" 1 "aendere Ladeleistung Donnerstag morgens Laden $mollp1doll A"
					fi
				fi
				if [ -z "$llnachtneu" ]; then
					llnachtneu=$llalt
				fi
			else
				nachtladen2state=0
			fi
		fi

		#Freitag
		if ((dayoftheweek == 5)); then
			if [[ "$currenttime" > "$mollp1frab" ]] && [[ "$currenttime" < "$mollp1frbis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1frll
					openwbDebugLog "CHARGESTAT" 0 "Freitag morgens Laden gestartet mit $mollp1frll A"
					openwbDebugLog "MAIN" 1 "Ladeleistung Freitag morgens Laden $mollp1frll A"
				else
					if ! grep -q "$mollp1frll" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1frll
						openwbDebugLog "MAIN" 1 "aendere Ladeleistung Freitag morgens Laden $mollp1frll A"
					fi
				fi
				if [ -z "$llnachtneu" ]; then
					llnachtneu=$llalt
				fi
			else
				nachtladen2state=0
			fi
		fi

		#Samstag
		if ((dayoftheweek == 6)); then
			if [[ "$currenttime" > "$mollp1saab" ]] && [[ "$currenttime" < "$mollp1sabis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1sall
					openwbDebugLog "CHARGESTAT" 0 "Samstag morgens Laden gestartet mit $mollp1sall A"
					openwbDebugLog "MAIN" 1 "Ladeleistung Samstag morgens Laden $mollp1sall A"
				else
					if ! grep -q "$mollp1sall" "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1sall
						openwbDebugLog "MAIN" 1 "aendere Ladeleistung Samstag morgens Laden $mollp1sall A"
					fi
				fi
				if [ -z "$llnachtneu" ]; then
					llnachtneu=$llalt
				fi
			else
				nachtladen2state=0
			fi
		fi

	else
		nachtladenstate=0
		nachtladen2state=0
	fi

	#Nachtladen S1
	if [[ $nachtladens1 == "1" ]]; then
		if ((nachtladenabuhrs1 <= 10#$H && 10#$H <= 24)) || ((0 <= 10#$H && 10#$H < nachtladenbisuhrs1)); then
			nachtladenstates1=1
			dayoftheweek=$(date +%w)
			currenthour=$(date +%k)
			if [[ $dayoftheweek -eq 0 && $currenthour -ge 14 ]] || [[ $dayoftheweek -ge 1 && $dayoftheweek -le 4 ]] || [[ $dayoftheweek -eq 5 && $currenthour -le 11 ]]; then
				diesersocs1=$nachtsocs1
			else
				diesersocs1=$nachtsoc1s1
			fi
			if [[ $socmodul1 != "none" ]]; then
				openwbDebugLog "MAIN" 1 "Nachtladen mit SoC-Modul $socmodul1"
				if ((soc1 <= diesersocs1)); then
					if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						llnachts1neu=$nachtlls1
						openwbDebugLog "MAIN" 1 "SoC $soc1 Ladeleistung Nachtladen bei $nachtlls1"
					fi
					if ! grep -q "$nachtlls1" "/var/www/html/openWB/ramdisk/llsolls1"; then
						llnachts1neu=$nachtlls1
						openwbDebugLog "MAIN" 1 "aendere Nacht-Ladeleistung auf $nachtlls1"
					fi
				else
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						llnachts1neu=0
					fi
				fi
			else
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
					llnachts1neu=$nachtlls1
					openwbDebugLog "MAIN" 1 "SoC $soc1 Ladeleistung Nachtladen $nachtlls1 A"
					openwbDebugLog "CHARGESTAT" 0 "start Nachtladung mit $nachtlls1"
				else
					if ! grep -q "$nachtlls1" "/var/www/html/openWB/ramdisk/llsolls1"; then
						llnachts1neu=$nachtlls1
						openwbDebugLog "MAIN" 1 "aendere Nacht-Ladeleistung auf $nachtlls1"
					fi
				fi
			fi
			if [ -z "$llnachts1neu" ]; then
				llnachts1neu=$llalts1
			fi
		else
			nachtladenstates1=0
		fi
		if ((nachtladen2abuhrs1 <= 10#$H)) && ((10#$H < nachtladen2bisuhrs1)); then
			nachtladen2states1=1

			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
				llnachts1neu=$nacht2lls1
				#runs/set-current.sh "$nacht2lls1" s1
				openwbDebugLog "MAIN" 1 "SoC $soc1 Ladeleistung Nachtladen $nacht2lls1 A"
			else
				if ! grep -q "$nacht2lls1" "/var/www/html/openWB/ramdisk/llsolls1"; then
					llnachts1neu=$nacht2lls1
					#runs/set-current.sh "$nacht2lls1" m
					openwbDebugLog "MAIN" 1 "aendere Nacht-Ladeleistung auf $nacht2lls1"
				fi
			fi
			if [ -z "$llnachts1neu" ]; then
				llnachts1neu=$llalts1
			fi
		else
			nachtladen2states1=0
		fi
	else
		nachtladenstates1=0
		nachtladen2states1=0
	fi
	echo $nachtladenstate >/var/www/html/openWB/ramdisk/nachtladenstate
	echo $nachtladenstates1 >/var/www/html/openWB/ramdisk/nachtladenstates1
	echo $nachtladen2state >/var/www/html/openWB/ramdisk/nachtladen2state
	echo $nachtladen2states1 >/var/www/html/openWB/ramdisk/nachtladen2states1
	if ((nachtladenstate == 1)) || ((nachtladenstates1 == 1)) || ((nachtladen2state == 1)) || ((nachtladen2states1 == 1)); then
		if ((nachtladenstate == 1)) || ((nachtladen2state == 1)); then
			lastmnacht "$llalt" "$llnachtneu"
			if ((llnachtreturn != llalt)); then
				runs/set-current.sh "$llnachtreturn" m
				openwbDebugLog "CHARGESTAT" 0 "LP1, Lademodus Nachtladen. Ladung mit $llnachtreturn Ampere, $diesersoc % SoC"
			fi
		fi
		if ((nachtladenstates1 == 1)) || ((nachtladen2states1 == 1)); then
			lastmnacht "$llalts1" "$llnachts1neu"
			if ((llnachtreturn != llalts1)); then
				runs/set-current.sh "$llnachtreturn" s1
				openwbDebugLog "CHARGESTAT" 0 "LP2, Lademodus Nachtladen. Ladung mit $llnachtreturn Ampere, $diesersocs1 % SoC"
			fi
		fi
		exit 0
	fi
}

prenachtlademodus() {
	if { ((lademodus == 0)) && ((nlakt_sofort == 1)); } || { ((lademodus == 1)) && ((nlakt_minpv == 1)); } || { ((lademodus == 2)) && ((nlakt_nurpv == 1)); } || { ((lademodus == 4)) && ((nlakt_standby == 1)); }; then
		nachtlademodus
	else
		echo 0 >ramdisk/nachtladenstate
		echo 0 >ramdisk/nachtladen2state
		echo 0 >ramdisk/nachtladenstates1
		echo 0 >ramdisk/nachtladen2states1
	fi
}
