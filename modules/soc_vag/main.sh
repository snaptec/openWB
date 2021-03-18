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
		fztype=$soc2type
		username=$soc2user
		password=$soc2pass
		vin=$soc2vin
		intervall=$(( soc2intervall * 6 ))
		intervallladen=$(( soc2intervallladen * 6 ))
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		ladeleistung=$(<$RAMDISKDIR/llaktuell)
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		fztype=$soc_vag_type
		username=$soc_vag_username
		password=$soc_vag_passwort
		vin=$soc_id_vin
		intervall=$(( soc_vag_intervall * 6 ))
		intervallladen=$(( soc_vag_intervallladen * 6 ))
		;;
esac

getAndWriteSoc(){
		echo 0 > $soctimerfile
		socDebugLog "Requesting SoC"
		echo 0 > $soctimerfile
		answer=$($MODULEDIR/../evcc-soc $fztype --user "$username" --password "$password" --vin "$vin" 2>&1)
		if [ $? -eq 0 ]; then
			# we got a valid answer
			echo $answer > $socfile
			socDebugLog "SoC: $answer"
		else
			# we have a problem
			socDebugLog "Error from evcc-soc: $answer"
		fi
}

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

soctimer=$(<$soctimerfile)
if (( ladeleistung > 500 )); then
	if (( soctimer < intervallladen )); then
		socDebugLog "Charging, but nothing to do yet. Incrementing timer."
		soctimer=$((soctimer+1))
		echo $soctimer > $soctimerfile
	else
		getAndWriteSoc
	fi
else
	if (( soctimer < intervall )); then
		socDebugLog "Nothing to do yet. Incrementing timer."
		soctimer=$((soctimer+1))
		echo $soctimer > $soctimerfile
	else
		getAndWriteSoc
	fi
fi
