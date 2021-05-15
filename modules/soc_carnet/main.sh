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
		intervall=$soccarnetlp2intervall
		username=$carnetlp2user
		password=$carnetlp2pass
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		intervall=$soccarnetintervall
		username=$carnetuser
		password=$carnetpass
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

reValidSoc='^-?[0-9]+$'

vwtimer=$(<$soctimerfile)
if (( vwtimer < 60 )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	vwtimer=$((vwtimer+1))
	echo $vwtimer > $soctimerfile
else
	socDebugLog "Requesting SoC"
	echo 0 > $soctimerfile

	response=$(sudo PYTHONIOENCODING=UTF-8 python $MODULEDIR/we_connect_client.py --user="$username" --password="$password")
	soclevel=$(echo "$response" | grep batteryPercentage | jq -r .EManager.rbc.status.batteryPercentage)
	socDebugLog "Filtered SoC from Server: $soclevel"
	if  [[ $soclevel =~ $reValidSoc ]] ; then
		if (( $soclevel != 0 )) ; then
			socDebugLog "SoC is valid"
			echo $soclevel > $socfile
		fi
	else
		socDebugLog "SoC is not valid."
		socDebugLog "Response from Server: ${response}"
	fi

	#Abfrage Ladung aktiv. Setzen des soctimers. 
	if (( ladeleistung > 800 )) ; then
		vwtimer=$((60 * (10 - $intervall) / 10))
		echo $vwtimer > $soctimerfile
	fi
fi
