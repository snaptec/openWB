#!/bin/bash
nrgkickcheck(){
	#######################################
	#nrgkick mobility check
	if [[ $evsecon == "nrgkick" ]]; then
		output=$(curl --connect-timeout 3 -s http://$nrgkickiplp1/api/settings/$nrgkickmaclp1)
		current=$(</var/www/html/openWB/ramdisk/llsoll)
		if [[ $? == "0" ]] ; then
			state=$(echo $output | jq -r '.Values.ChargingStatus.Charging')
			if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatus"; then
				if [[ $state == "false" ]] ; then
					curl --connect-timeout 2 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": true }, "ChargingCurrent": { "Value": $current }, "DeviceMetadata":{"Password": $nrgkickpwlp1}}}" $nrgkickiplp1/api/settings/$nrgkickmaclp1 > /dev/null
				fi
			fi
			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
				if [[ $state == "true" ]] ; then
				curl --connect-timeout 2 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": false }, "ChargingCurrent": { "Value": "6"}, "DeviceMetadata":{"Password": $nrgkickpwlp1}}}" $nrgkickiplp1/api/settings/$nrgkickmaclp1 > /dev/null
				fi
			fi
			oldcurrent=$(echo $output | jq -r '.Values.ChargingCurrent.Value')
			current=$(</var/www/html/openWB/ramdisk/llsoll)
			if (( oldcurrent != $current )) ; then
				curl --silent --connect-timeout $nrgkicktimeoutlp1 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": true }, "ChargingCurrent": { "Value": $current}, "DeviceMetadata":{"Password": $nrgkickpwlp1}}}" $nrgkickiplp1/api/settings/$nrgkickmaclp1 > /dev/null
				> /dev/null
				# BUG? remove line above?
			fi
		fi
	fi
	if [[ $evsecons1 == "nrgkick" ]]; then
		output=$(curl --connect-timeout 3 -s http://$nrgkickiplp2/api/settings/$nrgkickmaclp2)
		current=$(</var/www/html/openWB/ramdisk/llsolls1)
		if [[ $? == "0" ]] ; then
			state=$(echo $output | jq -r '.Values.ChargingStatus.Charging')
			if grep -q 1 "/var/www/html/openWB/ramdisk/ladestatuss1"; then
				if [[ $state == "false" ]] ; then
					curl --connect-timeout 2 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": true }, "ChargingCurrent": { "Value": $current }, "DeviceMetadata":{"Password": $nrgkickpwlp2}}}" $nrgkickiplp2/api/settings/$nrgkickmaclp2 > /dev/null
				fi
			fi
			if grep -q 0 "/var/www/html/openWB/ramdisk/ladestatus"; then
				if [[ $state == "true" ]] ; then
					curl --connect-timeout 2 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": false }, "ChargingCurrent": { "Value": "6"}, "DeviceMetadata":{"Password": $nrgkickpwlp2}}}" $nrgkickiplp2/api/settings/$nrgkickmaclp2 > /dev/null
				fi
			fi
			oldcurrent=$(echo $output | jq -r '.Values.ChargingCurrent.Value')
			current=$(</var/www/html/openWB/ramdisk/llsolls1)
			if (( oldcurrent != $current )) ; then
				curl --silent --connect-timeout $nrgkicktimeoutlp2 -s -X PUT -H "Content-Type: application/json" --data "{ "Values": {"ChargingStatus": { "Charging": true }, "ChargingCurrent": { "Value": $current}, "DeviceMetadata":{"Password": $nrgkickpwlp2}}}" $nrgkickiplp2/api/settings/$nrgkickmaclp2 > /dev/null
				> /dev/null
				# BUG? remove line above?
			fi
		fi
	fi
}
