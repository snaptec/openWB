#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
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
		username=$soc2user
		password=$soc2pass
		vin=$soc2vin
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		username=$soc_audi_username
		password=$soc_audi_passwort
		vin=$soc_audi_vin
		;;
esac

socDebugLog(){
	if (( $socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

auditimer=$(<$soctimerfile)
if (( auditimer < 180 )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	auditimer=$((auditimer+1))
	if ((ladeleistung > 800 )); then
		auditimer=$((auditimer+2))
	fi
	echo $auditimer > $soctimerfile
else
	echo 0 > $soctimerfile
	socDebugLog "Requesting SoC"
	answer=$($MODULEDIR/../evcc-soc audi --user "$username" --password "$passsword" --vin "$vin" 2>&1)
	if [ $? -eq 0 ]; then
 		# we got a valid answer
 		echo $answer > $socfile
 		socDebugLog "SoC: $answer"
 	else
 		# we have a problem
 		socDebugLog "Error from evcc-soc: $answer"
 	fi
fi
