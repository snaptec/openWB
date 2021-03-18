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
		intervall=$(( soc1intervall * 6 ))
		intervallladen=$(( soc1intervallladen * 6 ))
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

getAndWriteSoc(){
		echo 0 > $soctimerfile
		socDebugLog "Requesting SoC"
		echo 0 > $soctimerfile
		soc=$(curl --connect-timeout 15 -s $ip | cut -f1 -d".")
		if [ $soc -eq 0 ]; then
			# we got a valid answer
			echo $soc > $socfile
			socDebugLog "SoC: $soc"
		else
			# we have a problem
			socDebugLog "Error from http call: $soc"
		fi
}

#wenn SOC nicht verfügbar (keine Antwort) ersetze leeren Wert durch eine 0
#re='^[0-9]+$'
#if [[ $soc =~ $re ]] ; then
#	echo $soc > $socfile
#fi

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
