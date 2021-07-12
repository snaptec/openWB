#!/bin/bash
# initially created by Stefan Schefler for openWB 2019
# modified by Kevin Wieland
# based on Homematic Script v0.2 (c) 2018 by Alchy


# Daten einlesen
HTML=$(/usr/bin/curl -u $wr2_piko2_user:$wr2_piko2_pass --connect-timeout 10 -s -k $wr2_piko2_url | /usr/bin/tr -d '\r' | /usr/bin/tr -d '\n' | /usr/bin/tr -d ' ' | /usr/bin/tr '#' ' ')
# request html, concat to one line, remove spaces, add spaces before color changes (#)
 
if [[ -n $HTML ]]             # check if valid content of request
then
	counter=0
	for LINE in $HTML         # parse all html lines
	do
		if [[ $LINE =~ FFFFFF ]];   # search for white background color
		then
			((counter++))
			PART2=${LINE##*F\">}   # strip before number
			VALUE=${PART2%%<*}   # strip after number

			if [[ $counter -eq 1 ]]   # pvwatt
			then
				if [[ $VALUE = "xxx" ]]    # off-value equals zero
				then
					$VALUE = "0"
				fi
				re='^[-+]?[0-9]+\.?[0-9]*$'
				if ! [[ $VALUE =~ $re ]]   # check for valid number
				then
					VALUE=$(</var/www/html/openWB/ramdisk/pv2watt)
				fi
				echo $((VALUE*-1)) > /var/www/html/openWB/ramdisk/pv2watt
				echo $((VALUE*-1))
			elif [[ $counter -eq 2 ]]   # pvkwhk
			then
				echo ${VALUE} > /var/www/html/openWB/ramdisk/pv2kwhk
			fi
		fi
	done
fi
