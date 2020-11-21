#!/bin/bash
lastmnacht(){
	if [[ $schieflastaktiv == "1" ]]; then
		if [[ $u1p3paktiv == "1" ]]; then
			u1p3pstat=$(<ramdisk/u1p3pstat)
			if [[ $u1p3pstat == "1" ]]; then
				maximalstromstaerke=$schieflastmaxa
			fi
		fi
	fi
	if [ $# -eq 2 ]; then
		if (( evua1 < lastmaxap1 )) && (( evua2 < lastmaxap2 )) && (( evua3 < lastmaxap3 )); then
			evudiff1=$((lastmaxap1 - evua1 ))
			evudiff2=$((lastmaxap2 - evua2 ))
			evudiff3=$((lastmaxap3 - evua3 ))
			evudiffmax=($evudiff1 $evudiff2 $evudiff3)
			maxdiff=${evudiffmax[0]}
			for v in "${evudiffmax[@]}"; do
				if (( v < maxdiff )); then maxdiff=$v; fi;
			done
			if (( $1 == $2 )); then
				llnachtreturn=$2
			else
				if (( $2 == 0 )); then
					llnachtreturn=$2
				else
					if (( $1 > $2 )); then
						llnachtreturn=$(($1 - 1 ))
					else
						if (( maxdiff > 1 )); then
							llnachtreturn=$(($1 + 1 ))
						else
							llnachtreturn=$1
						fi
					fi
					if (( llnachtreturn > maximalstromstaerke )); then
						llnachtreturn=$2
					fi
					if (( llnachtreturn < minimalstromstaerke )); then
						llnachtreturn=$minimalstromstaerke
					fi
				fi
			fi
		else
			evudiff1=$((evua1 - lastmaxap1 ))
			evudiff2=$((evua2 - lastmaxap2 ))
			evudiff3=$((evua3 - lastmaxap3 ))
			evudiffmax=($evudiff1 $evudiff2 $evudiff3)
			maxdiff=0
			for vv in "${evudiffmax[@]}"; do
				if (( vv > maxdiff )); then maxdiff=$vv; fi;
			done
			maxdiff=$((maxdiff + 1 ))
			llnachtreturn=$(($1 - maxdiff))
			if (( llnachtreturn < minimalstromstaerke )); then
				llnachtreturn=$minimalstromstaerke
				if [[ $debug == "1" ]]; then
					echo Differenz groesser als minimalstromstaerke, setze Nachtladen auf minimal A $minimalstromstaerke
				fi
			fi
			echo "Lastmanagement aktiv, Ladeleistung reduziert" > ramdisk/lastregelungaktiv
			if [[ $debug == "1" ]]; then
				echo "Nachtladen um $maxdiff auf $llnachtreturn reduziert"
			fi
		fi
	fi
}

nachtlademodus(){
	if [[ $nachtladen == "1" ]]; then
		if (( nachtladenabuhr <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H < nachtladenbisuhr )); then
			nachtladenstate=1
			dayoftheweek=$(date +%w)
			currenthour=$(date +%k)
			if [[ $dayoftheweek -eq 0 && $currenthour -ge 14 ]] || [[ $dayoftheweek -ge 1 && $dayoftheweek -le 4 ]] || [[ $dayoftheweek -eq 5 && $currenthour -le 11 ]]  ; then
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
						llnachtneu=$nachtll
						#runs/set-current.sh "$nachtll" m
						if [[ $debug == "1" ]]; then
							echo "soc $soc"
							echo "ladeleistung nachtladen bei $nachtll"
						fi
					fi
					if ! grep -q $nachtll "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$nachtll
						#runs/set-current.sh "$nachtll" m
						if [[ $debug == "1" ]]; then
							echo aendere nacht Ladeleistung auf $nachtll
						fi
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
					if [[ $debug == "1" ]]; then
						echo "soc $soc"
						echo "ladeleistung nachtladen $nachtll A"
					fi
				else
					if ! grep -q $nachtll "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$nachtll
						#runs/set-current.sh "$nachtll" m
						if [[ $debug == "1" ]]; then
							echo aendere nacht Ladeleistung auf $nachtll
						fi
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
		if (( dayoftheweek == 0 )); then
			if [[ "$currenttime" > "$mollp1soab" ]] && [[ "$currenttime" < "$mollp1sobis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1soll
					echo "$date Sonntag morgens Laden gestartet mit $mollp1soll A" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "ladeleistung Sonntag morgens Laden $mollp1soll A"
					fi
				else
					if ! grep -q $mollp1soll "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1soll
						if [[ $debug == "1" ]]; then
							echo "aendere ladeleistung Sonntag morgens Laden $mollp1soll A"
						fi
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
		if (( dayoftheweek == 1 )); then
			if [[ "$currenttime" > "$mollp1moab" ]] && [[ "$currenttime" < "$mollp1mobis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1moll
					echo "$date Montag morgens Laden gestartet mit $mollp1moll A" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "ladeleistung Sonntag morgens Laden $mollp1moll A"
					fi
				else
					if ! grep -q $mollp1moll "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1moll
						if [[ $debug == "1" ]]; then
							echo "aendere ladeleistung Montag morgens Laden $mollp1moll A"
						fi
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
		if (( dayoftheweek == 2 )); then
			if [[ "$currenttime" > "$mollp1diab" ]] && [[ "$currenttime" < "$mollp1dibis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1dill
					echo "$date Dienstag morgens Laden gestartet mit $mollp1dill A" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "ladeleistung Dienstag morgens Laden $mollp1dill A"
					fi
				else
					if ! grep -q $mollp1dill "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1dill
						if [[ $debug == "1" ]]; then
							echo "aendere ladeleistung Dienstag morgens Laden $mollp1dill A"
						fi
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
		if (( dayoftheweek == 3 )); then
			if [[ "$currenttime" > "$mollp1miab" ]] && [[ "$currenttime" < "$mollp1mibis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1mill
					echo "$date Mittwoch morgens Laden gestartet mit $mollp1mill A" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "ladeleistung Mittwoch morgens Laden $mollp1mill A"
					fi
				else
					if ! grep -q $mollp1mill "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1mill
						if [[ $debug == "1" ]]; then
							echo "aendere ladeleistung Mittwoch morgens Laden $mollp1mill A"
						fi
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
		if (( dayoftheweek == 4 )); then
			if [[ "$currenttime" > "$mollp1doab" ]] && [[ "$currenttime" < "$mollp1dobis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1doll
					echo "$date Donnerstag morgens Laden gestartet mit $mollp1doll A" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "ladeleistung Donnerstag morgens Laden $mollp1doll A"
					fi
				else
					if ! grep -q $mollp1doll "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1doll
						if [[ $debug == "1" ]]; then
							echo "aendere ladeleistung Donnerstag morgens Laden $mollp1doll A"
						fi
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
		if (( dayoftheweek == 5 )); then
			if [[ "$currenttime" > "$mollp1frab" ]] && [[ "$currenttime" < "$mollp1frbis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1frll
					echo "$date Freitag morgens Laden gestartet mit $mollp1frll A" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "ladeleistung Freitag morgens Laden $mollp1frll A"
					fi
				else
					if ! grep -q $mollp1frll "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1frll
						if [[ $debug == "1" ]]; then
							echo "aendere ladeleistung Freitag morgens Laden $mollp1frll A"
						fi
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
		if (( dayoftheweek == 6 )); then
			if [[ "$currenttime" > "$mollp1saab" ]] && [[ "$currenttime" < "$mollp1sabis" ]]; then
				nachtladen2state=1
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					llnachtneu=$mollp1sall
					echo "$date Samstag morgens Laden gestartet mit $mollp1sall A" >> ramdisk/ladestatus.log
					if [[ $debug == "1" ]]; then
						echo "ladeleistung Samstag morgens Laden $mollp1sall A"
					fi
				else
					if ! grep -q $mollp1sall "/var/www/html/openWB/ramdisk/llsoll"; then
						llnachtneu=$mollp1sall
						if [[ $debug == "1" ]]; then
							echo "aendere ladeleistung Samstag morgens Laden $mollp1sall A"
						fi
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
		if (( nachtladenabuhrs1 <= 10#$H && 10#$H <= 24 )) || (( 0 <= 10#$H && 10#$H < nachtladenbisuhrs1 )); then
			nachtladenstates1=1
			dayoftheweek=$(date +%w)
			currenthour=$(date +%k)
			if [[ $dayoftheweek -eq 0 && $currenthour -ge 14 ]] || [[ $dayoftheweek -ge 1 && $dayoftheweek -le 4 ]] || [[ $dayoftheweek -eq 5 && $currenthour -le 11 ]]  ; then
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
						llnachts1neu=$nachtlls1
						#runs/set-current.sh "$nachtlls1" s1
						if [[ $debug == "1" ]]; then
							echo "soc $soc1"
							echo "ladeleistung nachtladen bei $nachtlls1"
						fi
					fi
					if ! grep -q $nachtlls1 "/var/www/html/openWB/ramdisk/llsolls1"; then
						llnachts1neu=$nachtlls1
						#runs/set-current.sh "$nachtlls1" s1
						if [[ $debug == "1" ]]; then
							echo aendere nacht Ladeleistung auf $nachtlls1
						fi
					fi
				else
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						llnachts1neu=0
						#runs/set-current.sh 0 s1
					fi
				fi
			else
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
					llnachts1neu=$nachtlls1
					#runs/set-current.sh "$nachtlls1" s1
					if [[ $debug == "1" ]]; then
						echo "soc $soc1"
						echo "ladeleistung nachtladen $nachtlls1 A"
					fi
					echo "start Nachtladung mit $nachtlls1 um $date" >> web/lade.log
				else
					if ! grep -q $nachtlls1 "/var/www/html/openWB/ramdisk/llsolls1"; then
						llnachts1neu=$nachtlls1
						#runs/set-current.sh "$nachtlls1" s1
						if [[ $debug == "1" ]]; then
							echo aendere nacht Ladeleistung auf $nachtlls1
						fi
					fi
				fi
			fi
			if [ -z "$llnachts1neu" ]; then
				llnachts1neu=$llalts1
			fi
		else
			nachtladenstates1=0
		fi
		if (( nachtladen2abuhrs1 <= 10#$H )) && (( 10#$H < nachtladen2bisuhrs1 )); then
			nachtladen2states1=1
			dayoftheweek=$(date +%w)

			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
				llnachts1neu=$nacht2lls1
				#runs/set-current.sh "$nacht2lls1" s1
				if [[ $debug == "1" ]]; then
					echo "soc $soc1"
					echo "ladeleistung nachtladen $nacht2lls1 A"
				fi
			else
				if ! grep -q $nacht2lls1 "/var/www/html/openWB/ramdisk/llsolls1"; then
					llnachts1neu=$nacht2lls1
					#runs/set-current.sh "$nacht2lls1" m
					if [[ $debug == "1" ]]; then
						echo aendere nacht Ladeleistung auf $nacht2lls1
					fi
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
	echo $nachtladenstate > /var/www/html/openWB/ramdisk/nachtladenstate
	echo $nachtladenstates1 > /var/www/html/openWB/ramdisk/nachtladenstates1
	echo $nachtladen2state > /var/www/html/openWB/ramdisk/nachtladen2state
	echo $nachtladen2states1 > /var/www/html/openWB/ramdisk/nachtladen2states1
	if (( nachtladenstate == 1 )) || (( nachtladenstates1 == 1 )) || (( nachtladen2state == 1 )) || (( nachtladen2states1 == 1 )); then
		if (( nachtladenstate == 1 )) || (( nachtladen2state == 1 )); then
			lastmnacht $llalt $llnachtneu 
			if (( llnachtreturn != llalt )); then
				runs/set-current.sh $llnachtreturn m
				echo "$date LP1, Lademodus Nachtladen. Ladung mit $llnachtreturn Ampere, $diesersoc % SoC" >> ramdisk/ladestatus.log
			fi
		fi
		if (( nachtladenstates1 == 1 )) || (( nachtladen2states1 == 1 )); then
			lastmnacht $llalts1 $llnachts1neu
			if (( llnachtreturn != llalts1 )); then
				runs/set-current.sh $llnachtreturn s1
				echo "$date LP2, Lademodus Nachtladen. Ladung mit $llnachtreturn Ampere, $diesersocs1 % SoC" >> ramdisk/ladestatus.log
			fi
		fi
		exit 0
	fi
}

prenachtlademodus(){
	if { (( lademodus == 0 )) && (( nlakt_sofort == 1 )); } || { (( lademodus == 1 )) && (( nlakt_minpv == 1 )); } || { (( lademodus == 2 )) && (( nlakt_nurpv == 1 )); } || { (( lademodus == 4 )) && (( nlakt_standby == 1 )); } then
		nachtlademodus
	else
		echo 0 > ramdisk/nachtladenstate
		echo 0 > ramdisk/nachtladen2state
		echo 0 > ramdisk/nachtladenstates1
		echo 0 > ramdisk/nachtladen2states1
	fi
}
