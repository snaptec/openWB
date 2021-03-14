#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULE="EVU"
#LOGFILE="$RAMDISKDIR/speicher.log"
LOGFILE="$RAMDISKDIR/openWB.log"
Debug=$debug
myPid=$$

#For Development only
#Debug=1

COOKIEFILE="$RAMDISKDIR/powerwall_cookie.txt"
cookieOptions=""

DebugLog(){
	if (( Debug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		if (( Debug == 2 )); then
			echo "$timestamp: ${MODULE}: PID:$myPid: $@" >> $LOGFILE
		else
			echo "$timestamp: ${MODULE}: $@" >> $LOGFILE
		fi
	fi
}

if (( speicherpwloginneeded == 1 )); then
	# delete our login cookie after some time as it may be invalid
	if [[ $(find "$COOKIEFILE" -cmin +60) ]]; then
		DebugLog "Deleting saved login cookie after 1 hour as it may not be valid anymore."
		rm "$COOKIEFILE"
	fi
	if [[ ! -f "$COOKIEFILE" ]]; then
		# log in and save cookie for later use
		DebugLog "Trying to authenticate..."
		curl -s -k -i -c $COOKIEFILE --connect-timeout 5 -X POST -H "Content-Type: application/json" -d "{\"username\":\"customer\",\"password\":\"$speicherpwpass\", \"email\":\"$speicherpwuser\",\"force_sm_off\":false}" "https://$speicherpwip/api/login/Basic"
		exitCode=$?
		if (( exitCode != 0 )); then
			DebugLog "Something went wrong. Curl Exit Code: $exitCode"
			exit
		else
			DebugLog "Login successfull."
		fi
	else
		DebugLog "Using saved login cookie."
	fi
	# tell next curl calls to use saved cookie
	cookieOptions="-b $COOKIEFILE -c $COOKIEFILE"
fi

answer=$(curl -k $cookieOptions --connect-timeout 5 -s "https://$speicherpwip/api/meters/aggregates")
evuwatt=$(echo $answer | jq -r '.site.instant_power'  | sed 's/\..*$//')
echo $evuwatt
echo $evuwatt > /var/www/html/openWB/ramdisk/wattbezug
evuikwh=$(echo $answer | jq -r '.site.energy_imported')
echo $evuikwh > /var/www/html/openWB/ramdisk/bezugkwh
evuekwh=$(echo $answer | jq -r '.site.energy_exported')
echo $evuekwh > /var/www/html/openWB/ramdisk/einspeisungkwh

answer=$(curl -k $cookieOptions --connect-timeout 5 -s "https://$speicherpwip/api/status")
powerwallfirmwareversion=$(echo $answer | jq -r '.version' | sed 's/\.//g' )
echo $powerwallfirmwareversion > /var/www/html/openWB/ramdisk/powerwallfirmwareversion

if (( $powerwallfirmwareversion >= 20490 )); then
	answer=$(curl -k $cookieOptions --connect-timeout 5 -s "https://$speicherpwip/api/meters/site")
	evuv1=$(echo $answer | jq -r '.[0].Cached_readings.v_l1n')
	echo $evuv1 > /var/www/html/openWB/ramdisk/evuv1
	evuv2=$(echo $answer | jq -r '.[0].Cached_readings.v_l2n')
	echo $evuv2 > /var/www/html/openWB/ramdisk/evuv2
	evuv3=$(echo $answer | jq -r '.[0].Cached_readings.v_l3n')
	echo $evuv3 > /var/www/html/openWB/ramdisk/evuv3
	bezuga1=$(echo $answer | jq -r '.[0].Cached_readings.i_a_current')
	echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
	bezuga2=$(echo $answer | jq -r '.[0].Cached_readings.i_b_current')
	echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
	bezuga3=$(echo $answer | jq -r '.[0].Cached_readings.i_c_current')
	echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3
	bezugw1=$(echo $answer | jq -r '.[0].Cached_readings.real_power_a')
	echo $bezugw1 > /var/www/html/openWB/ramdisk/bezugw1
	bezugw2=$(echo $answer | jq -r '.[0].Cached_readings.real_power_b')
	echo $bezugw2 > /var/www/html/openWB/ramdisk/bezugw2
	bezugw3=$(echo $answer | jq -r '.[0].Cached_readings.real_power_c')
	echo $bezugw3 > /var/www/html/openWB/ramdisk/bezugw3
fi
