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
		socfile="$RAMDISKDIR/soc1"
		ip=$hsocip1
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		socfile="$RAMDISKDIR/soc"
		ip=$hsocip
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

socDebugLog "Requesting SoC"
soc=$(curl --connect-timeout 15 -s $ip | cut -f1 -d".")

#wenn SOC nicht verfügbar (keine Antwort) ersetze leeren Wert durch eine 0
re='^[0-9]+$'
if [[ $soc =~ $re ]] ; then
	echo $soc > $socfile
fi
