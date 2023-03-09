#!/bin/bash
goecheck(){
	#######################################
	#goe mobility check
	digit='^[0-9]$'

	if [[ $evsecon == "goe" ]]; then
		output=$(curl --connect-timeout 1 -s http://$goeiplp1/status)
		if [[ $? == "0" ]] ; then
			#check whether goe has 1to3phase switch capability => new HWV3 and new API V2
			fsp=$(echo $output | jq -r '.fsp')
			if [[ ! $fsp =~ $digit ]] ; then
				state=$(echo $output | jq -r '.alw')
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
					lp1enabled=$(</var/www/html/openWB/ramdisk/lp1enabled)
					if ((state == "0"))	 && (( lp1enabled == "1" )) ; then
						curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=alw=1 > /dev/null
					fi
				fi
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					if ((state == "1")) ; then
						curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=alw=0 > /dev/null
					fi
				fi
				version=$(echo $output | jq -r '.fwv')	# get firmware version
				majorVersion=${version%.*}				# remove everything after a "."
				majorVersion=${majorVersion%-*}			# remove everything after a "-"
				majorVersion=${majorVersion#0}			# remove leading "0"


				oldcurrent=$(echo $output | jq -r '.amp')
				current=$(</var/www/html/openWB/ramdisk/llsoll)
				if (( oldcurrent != $current )) && (( $current != 0 )); then
					if (($majorVersion >= 40)) ; then
						curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=amx=$current > /dev/null
					else
						curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/mqtt?payload=amp=$current > /dev/null
					fi
				fi
			else
				output=$(curl --connect-timeout 1 -s http://$goeiplp1/api/status)
				state=$(echo $output | jq -r '.frc')
				if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
					lp1enabled=$(</var/www/html/openWB/ramdisk/lp1enabled)
					if ((state == "1"))	 && (( lp1enabled == "1" )) ; then
						curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/api/set?frc=0 > /dev/null
					fi
				fi
				if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
					if (( state == "0" )) || (( state == "2" )) ; then
						curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/api/set?frc=1 > /dev/null
					fi
				fi
				oldcurrent=$(echo $output | jq -r '.amp')
				current=$(</var/www/html/openWB/ramdisk/llsoll)
				if (( oldcurrent != $current )) && (( $current != 0 )) ; then
					curl --silent --connect-timeout $goetimeoutlp1 -s http://$goeiplp1/api/set?amp=$current > /dev/null
				fi
			fi
		fi
	fi
	if [[ $lastmanagement == "1" ]]; then
		if [[ $evsecons1 == "goe" ]]; then
			output=$(curl --connect-timeout 1 -s http://$goeiplp2/status)
			if [[ $? == "0" ]] ; then
				#check whether goe has 1to3phase switch capability => new HWV3 and new API V2
				fsp=$(echo $output | jq -r '.fsp')
				if [[ ! $fsp =~ $digit ]] ; then
					state=$(echo $output | jq -r '.alw')
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						lp2enabled=$(</var/www/html/openWB/ramdisk/lp2enabled)
						if ((state == "0"))	 && (( lp2enabled == "1" )) ; then
							curl --silent --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/mqtt?payload=alw=1 > /dev/null
						fi
					fi
					if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						if ((state == "1")) ; then
							curl --silent --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/mqtt?payload=alw=0 > /dev/null
						fi
					fi
					version=$(echo $output | jq -r '.fwv')	# get firmware version
					majorVersion=${version%.*}				# remove everything after a "."
					majorVersion=${majorVersion%-*}			# remove everything after a "-"
					majorVersion=${majorVersion#0}			# remove leading "0"

					oldcurrent=$(echo $output | jq -r '.amp')
					current=$(</var/www/html/openWB/ramdisk/llsolls1)
					if (( oldcurrent != $current )) && (( $current != 0 )); then
						if (($majorVersion >= 40)) ; then
							curl --silent --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/mqtt?payload=amx=$current > /dev/null
						else
							curl --silent --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/mqtt?payload=amp=$current > /dev/null
						fi
					fi
				else
					output=$(curl --connect-timeout 1 -s http://$goeiplp2/api/status)
					state=$(echo $output | jq -r '.frc')
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						lp2enabled=$(</var/www/html/openWB/ramdisk/lp2enabled)
						if ((state == "1"))	 && (( lp2enabled == "1" )) ; then
							curl --silent --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/api/set?frc=0 > /dev/null
						fi
					fi
					if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
						if (( state == "0" )) || (( state == "2" )) ; then
							curl --silent --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/api/set?frc=1 > /dev/null
						fi
					fi
					oldcurrent=$(echo $output | jq -r '.amp')
					current=$(</var/www/html/openWB/ramdisk/llsolls1)
					if (( oldcurrent != $current )) && (( $current != 0 )) ; then
						curl --silent --connect-timeout $goetimeoutlp2 -s http://$goeiplp2/api/set?amp=$current > /dev/null
					fi
				fi
			fi
		fi
		if [[ $lastmanagements2 == "1" ]]; then
			if [[ $evsecons2 == "goe" ]]; then
			output=$(curl --connect-timeout 1 -s http://$goeiplp3/status)
			if [[ $? == "0" ]] ; then
				#check whether goe has 1to3phase switch capability => new HWV3 and new API V2
				fsp=$(echo $output | jq -r '.fsp')
				if [[ ! $fsp =~ $digit ]] ; then
					state=$(echo $output | jq -r '.alw')
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
						lp3enabled=$(</var/www/html/openWB/ramdisk/lp3enabled)
						if ((state == "0"))	 && (( lp3enabled == "1" )) ; then
							curl --silent --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/mqtt?payload=alw=1 > /dev/null
						fi
					fi
					if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
						if ((state == "1")) ; then
							curl --silent --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/mqtt?payload=alw=0 > /dev/null
						fi
					fi

					version=$(echo $output | jq -r '.fwv')	# get firmware version
					majorVersion=${version%.*}				# remove everything after a "."
					majorVersion=${majorVersion%-*}			# remove everything after a "-"
					majorVersion=${majorVersion#0}			# remove leading "0"

					oldcurrent=$(echo $output | jq -r '.amp')
					current=$(</var/www/html/openWB/ramdisk/llsolls2)
					if (( oldcurrent != $current )) ; then
						if (($majorVersion >= 40)) ; then
							curl --silent --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/mqtt?payload=amx=$current > /dev/null
						else
							curl --silent --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/mqtt?payload=amp=$current > /dev/null
						fi
					fi
				else
					output=$(curl --connect-timeout 1 -s http://$goeiplp3/api/status)
					state=$(echo $output | jq -r '.frc')
					if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
						lp3enabled=$(</var/www/html/openWB/ramdisk/lp3enabled)
						if (( state == "1" ))  && (( lp3enabled == "1" )) ; then
							curl --silent --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/api/set?frc=0 > /dev/null
						fi
					fi
					if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatuss2"; then
						if (( state == "0" )) || (( state == "2" )) ; then
							curl --silent --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/api/set?frc=1 > /dev/null
						fi
					fi
					oldcurrent=$(echo $output | jq -r '.amp')
					current=$(</var/www/html/openWB/ramdisk/llsolls2)
					if (( oldcurrent != $current && $current != 0 )) ; then
						curl --silent --connect-timeout $goetimeoutlp3 -s http://$goeiplp3/api/set?amp=$current > /dev/null
					fi
				fi
			fi
			fi
		fi
	fi
}
