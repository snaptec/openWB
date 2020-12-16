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
		bluelink_email=$soc2user
		bluelink_password=$soc2pass
		# bluelink_pin=$soc2pin # not needed at 2020-12-16
		bluelink_intervall=20
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		bluelink_email=$soc_bluelink_email
		bluelink_password=$soc_bluelink_password
		# bluelink_pin=$soc_bluelink_pin # not needed at 2020-12-16
		bluelink_intervall=$soc_bluelink_interval
		;;
esac

socDebugLog(){
	if (( $socDebug > 0 )); then
		timestamp=`date --rfc-3339=seconds`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

soctimervalue=$(<$soctimerfile)

tmpintervall=$(( bluelink_intervall * 6 ))

socDebugLog "SoCtimer: $soctimervalue, SoCIntervall: $tmpintervall"

if (( soctimervalue < tmpintervall )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	soctimervalue=$((soctimervalue+1))
	echo $soctimervalue > $soctimerfile
else
	socDebugLog "Requesting SoC"
	$MODULEDIR/../evcc-soc hyundai --user "$soc_bluelink_email" --password "$soc_bluelink_password" > $socfile &
	echo 0 > $soctimerfile
fi
