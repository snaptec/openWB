#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_i3: seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
fi

socDebug=$debug
# for developement only
#socDebug=1

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

incrementTimer(){
	case $dspeed in
		1)
			# Regelgeschwindigkeit 10 Sekunden
			ticksize=1
			;;
		2)
			# Regelgeschwindigkeit 20 Sekunden
			ticksize=2
			;;
		3)
			# Regelgeschwindigkeit 60 Sekunden
			ticksize=1
			;;
		*)
			# Regelgeschwindigkeit unbekannt
			ticksize=1
			;;
	esac
	soctimer=$((soctimer+$ticksize))
	echo $soctimer > $soctimerfile
}

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
cd /var/www/html/openWB/modules/soc_i3
if (( soctimer < 60 )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
	incrementTimer
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > $soctimerfile
	re='^-?[0-9]+$'
	abfrage=$(sudo php index.php --chargepoint=$CHARGEPOINT --username=$user --password=$pass --vin=$vin | jq '.')
	soclevel=$(echo $abfrage | jq '.chargingLevel')
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			echo $soclevel > $socfile
		fi
	fi
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC: $soclevel"

	#Abfrage Ladung aktiv. Setzen des soctimers.
	charging=$(echo $abfrage | jq '.chargingActive')
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Charging: $charging"
	if [[ $charging != 0 ]] ; then
		soctimer=$((60 * (10 - $intervall) / 10))
		echo $soctimer > $soctimerfile
	fi

	#Benachrichtigung bei Ladeabbruch
	error=$(echo $abfrage | jq '.chargingError')
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: chargingEror: $error"
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
