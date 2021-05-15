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
		ladeleistung=$(<$RAMDISKDIR/llaktuells1)
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
		ladeleistung=$(<$RAMDISKDIR/llaktuell)
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		username=$soc_id_username
		password=$soc_id_passwort
		vin=$soc_id_vin
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

soctimer=$(<$soctimerfile)

tmpintervall=$(( 480 * 6 ))

if (( soctimer < tmpintervall )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	soctimer=$((soctimer+1))
	if (( ladeleistung > 500 ));then
		socDebugLog "Car is charging"
		soctimer=$((soctimer+47))
	fi
	echo $soctimer > $soctimerfile
else
	socDebugLog "Requesting SoC"
	echo 0 > $soctimerfile
	answer=$($MODULEDIR/../evcc-soc id --user "$username" --password "$password" --vin "$vin" 2>&1)
	if [ $? -eq 0 ]; then
		# we got a valid answer
		echo $answer > $socfile
		socDebugLog "SoC: $answer"
	else
		# we have a problem
		socDebugLog "Error from evcc-soc: $answer"
	fi
fi
