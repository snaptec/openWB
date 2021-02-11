#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1

socDebug=$debug
# for developement only
socDebug=1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		akey=$evnotifyakeylp2
		token=$evnotifytokenlp2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		akey=$evnotifyakey
		token=$evnotifytoken
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

soctimer=$(<$soctimerfile)

if (( soctimer < 4 )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	soctimer=$((soctimer+1))
	echo $soctimer > $soctimerfile
else
	socDebugLog "Requesting SoC"
	echo 0 > $soctimerfile
	answer=$(curl -s -X GET 'https://app.evnotify.de/soc?akey='$akey'&token='$token)
	# extract the soc value
	soc=$(echo $answer | jq .soc_display)
	socDebugLog "SoC from Server: $soc"
	# parse to int to be able to check in condition - to determine if valid or not
	isvalid=$(echo $soc | cut -d "." -f 1 | cut -d "," -f 1)
	if (( isvalid >= 0 && isvalid != null)); then
		echo $isvalid > $socfile
	else
		socDebugLog "SoC is invalid!"
	fi
fi
