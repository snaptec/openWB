#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULE="BATT"
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

# read current load
speicherwatttmp=$(curl -k $cookieOptions --connect-timeout 5 -s "https://$speicherpwip/api/meters/aggregates")
speicherwatt=$(echo $speicherwatttmp | jq .battery.instant_power | sed 's/\..*$//')
speicherwatt=$(echo "$speicherwatt * -1" | bc)
ra='^[-+]?[0-9]+\.?[0-9]*$'
if ! [[ $speicherwatt =~ $ra ]] ; then
	speicherwatt="0"
fi
echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung

# read current SoC
speichersoc=$(curl -k $cookieOptions --connect-timeout 5 -s "https://$speicherpwip/api/system_status/soe")
soc=$(echo $speichersoc | jq .percentage)
soc=$(echo "($soc+0.5)/1" | bc)
if ! [[ $soc =~ $ra ]] ; then
	soc="0"
fi
echo $soc > /var/www/html/openWB/ramdisk/speichersoc
