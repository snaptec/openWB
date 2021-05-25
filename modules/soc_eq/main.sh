#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
MYLOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1
myPid=$$

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_eq: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

socDebug=$debug
# for developement only
#socDebug=1


case $CHARGEPOINT in
	2)
		# second charge point
		ladeleistungfile="$RAMDISKDIR/llaktuells1"
		soctimerfile="$RAMDISKDIR/soctimer1"
		soc_file="$RAMDISKDIR/soc1"
		soc_eq_client_id=$soc_eq_client_id_lp2
		soc_eq_client_secret=$soc_eq_client_secret_lp2
		soc_eq_vin=$soc_eq_vin_lp2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		ladeleistungfile="$RAMDISKDIR/llaktuell"
		soctimerfile="$RAMDISKDIR/soctimer"
		soc_file="$RAMDISKDIR/soc"
		soc_eq_client_id=$soc_eq_client_id_lp1
		soc_eq_client_secret=$soc_eq_client_secret_lp1
		soc_eq_vin=$soc_eq_vin_lp1
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
ladeleistung=$(<$ladeleistungfile)

if (( ladeleistung > 500 ));then
	tmpintervall=$(( 5 * 6 ))
else
	tmpintervall=$(( 60 * 6 ))
fi
if (( socDebug > 0 )); then
	tmpintervall=6
fi

if (( soctimer < tmpintervall )); then
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer. ${soctimer} < ${tmpintervall}"
	incrementTimer
else
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > $soctimerfile
	$MODULEDIR/soc.py $soc_eq_client_id $soc_eq_client_secret $soc_eq_vin $soc_file $CHARGEPOINT >>$MYLOGFILE 2>&1
	ret=$?
	openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Py Return: ${ret}"
	openwbModulePublishState "EVSOC" "${ret}" "Code: ${ret}" "$CHARGEPOINT"
fi
