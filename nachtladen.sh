#!/bin/bash
nachtlademodus(){

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
	if (( nachtladen2abuhr <= 10#$H )) && (( 10#$H < nachtladen2bisuhr )); then
		nachtladen2state=1
		dayoftheweek=$(date +%w)

			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
 				runs/set-current.sh "$nacht2ll" m
 				if [[ $debug == "1" ]]; then
      					echo "soc $soc"
        				echo "ladeleistung nachtladen $nacht2ll A"
        			fi
			else
				if ! grep -q $nacht2ll "/var/www/html/openWB/ramdisk/llsoll"; then
					runs/set-current.sh "$nacht2ll" m
					if [[ $debug == "1" ]]; then
      						echo aendere nacht Ladeleistung auf $nacht2ll
        				fi
				fi
			fi
		
	else
		nachtladen2state=0
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
	if (( nachtladen2abuhrs1 <= 10#$H )) && (( 10#$H < nachtladen2bisuhrs1 )); then
		nachtladen2states1=1
		dayoftheweek=$(date +%w)

			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
 				runs/set-current.sh "$nacht2lls1" s1
 				if [[ $debug == "1" ]]; then
      					echo "soc $soc1"
        				echo "ladeleistung nachtladen $nacht2lls1 A"
        			fi
			else
				if ! grep -q $nacht2lls1 "/var/www/html/openWB/ramdisk/llsolls1"; then
					runs/set-current.sh "$nacht2lls1" m
					if [[ $debug == "1" ]]; then
      						echo aendere nacht Ladeleistung auf $nacht2lls1
        				fi
				fi
			fi
		
	else
		nachtladen2states1=0
	fi

else
	nachtladenstates1=0
fi
echo $nachtladenstate > /var/www/html/openWB/ramdisk/nachtladenstate
echo $nachtladenstates1 > /var/www/html/openWB/ramdisk/nachtladenstates1
echo $nachtladen2state > /var/www/html/openWB/ramdisk/nachtladen2state
echo $nachtladen2states1 > /var/www/html/openWB/ramdisk/nachtladen2states1
if (( nachtladenstate == 1 )) || (( nachtladenstates1 == 1 )) || (( nachtladen2state == 1 )); then
	exit 0
fi
}
