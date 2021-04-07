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

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

getAndWriteSoc(){
	re='^-?[0-9]+$'
	openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Requesting SoC"
	echo 0 > $soctimerfile
	soc=$(curl --connect-timeout 15 -s $ip | cut -f1 -d".")
		
	if  [[ $soc =~ $re ]] ; then
		if (( $soc != 0 )) ; then
			echo $soc > $soc_file
			openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: SoC: $soc"
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
if (( ladeleistung > 500 )); then
	if (( soctimer < intervallladen )); then
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Charging, but nothing to do yet. Incrementing timer."
		soctimer=$((soctimer+1))
		echo $soctimer > $soctimerfile
	else
		getAndWriteSoc
	fi
else
	if (( soctimer < intervall )); then
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer."
		soctimer=$((soctimer+1))
		echo $soctimer > $soctimerfile
	else
		getAndWriteSoc
	fi
fi
