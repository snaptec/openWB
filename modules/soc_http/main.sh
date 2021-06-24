#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_http: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

case $CHARGEPOINT in
	2)
		# second charge point
		ladeleistung=$(<$RAMDISKDIR/llaktuells1)
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		ip=$hsocip1
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
		ip=$hsocip
		intervall=$(( soc_http_intervall * 6 ))
		intervallladen=$(( soc_http_intervallladen * 6 ))
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

getAndWriteSoc(){
	re='^-?[0-9]+$'
	openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > $soctimerfile
	soc=$(curl --connect-timeout 15 -s $ip | cut -f1 -d".")
		
	if  [[ $soc =~ $re ]] ; then
		if (( $soc != 0 )) ; then
			echo $soc > $socfile
			openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: SoC: $soc"
		else
		# we have a problem
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Error from http call"
		fi
	else
		# we have a problem
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Error from http call"
	fi
}

soctimer=$(<$soctimerfile)
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: timer = $soctimer"
if (( ladeleistung > 500 )); then
	if (( soctimer < intervallladen )); then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Charging, but nothing to do yet. Incrementing timer."
		incrementTimer
	else
		getAndWriteSoc
	fi
else
	if (( soctimer < intervall )); then
		openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		incrementTimer
	else
		getAndWriteSoc
	fi
fi
