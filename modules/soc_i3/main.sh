#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_i3: seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
fi

socDebug=$debug
# for developement only
socDebug=1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		intervall=$soci3intervall1
		user=$i3usernames1
		pass=$i3passworts1
		vin=$i3vins1
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		intervall=$soci3intervall
		user=$i3username
		pass=$i3passwort
		vin=$i3vin
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

i3timer=$(<$soctimerfile)
cd /var/www/html/openWB/modules/soc_i3
if (( i3timer < 60 )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	i3timer=$((i3timer+1))
	echo $i3timer > $soctimerfile
else
	socDebugLog "Requesting SoC"
	echo 0 > $soctimerfile
	re='^-?[0-9]+$'
	abfrage=$(sudo php index.php --chargepoint=$CHARGEPOINT --username=$user --password=$pass --vin=$vin | jq '.')
	soclevel=$(echo $abfrage | jq '.chargingLevel')
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > $socfile
		fi
	fi
	socDebugLog "SoC: $soclevel"

	#Abfrage Ladung aktiv. Setzen des soctimers.
	charging=$(echo $abfrage | jq '.chargingActive')
	socDebugLog "Charging: $charging"
	if [[ $charging != 0 ]] ; then
		soctimer=$((60 * (10 - $intervall) / 10))
		echo $soctimer > $soctimerfile
	fi

	#Benachrichtigung bei Ladeabbruch
	error=$(echo $abfrage | jq '.chargingError')
	socDebugLog "chargingEror: $error"
	if [[ $error == 1 ]] && [[ $pushbenachrichtigung == 1 ]] ; then
		#Abfrage, ob Fehler schon dokumentiert
		chargingError=$(<$RAMDISKDIR/chargingerror)
		#wiederholte Benachrichtigungen verhindern
		if [[ $chargingError == 0 ]] ; then
			message="ACHTUNG - Ladung bei "
			message+="$soclevel"
			message+="% abgebrochen"
			/var/www/html/openWB/runs/pushover.sh "$message"
			#dokumetieren des Fehlers in der Ramdisk
			echo 1 > $RAMDISKDIR/chargingerror
		fi
	else
		echo 0 > $RAMDISKDIR/chargingerror
	fi
fi
