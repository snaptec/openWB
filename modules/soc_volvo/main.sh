#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"
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
		username=$soc2user
		password=$soc2pass
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		username=$socuser
		password=$socpass
		;;
esac

socDebugLog(){
	if (( socDebug > 0 )); then
		timestamp=`date +"%Y-%m-%d %H:%M:%S"`
		echo "$timestamp: Lp$CHARGEPOINT: $@" >> $LOGFILE
	fi
}

soctimer=$(<$soctimerfile)

if (( soctimer < 60 )); then
	socDebugLog "Nothing to do yet. Incrementing timer."
	soctimer=$((soctimer+1))
	echo $soctimer > $soctimerfile
else
	echo 0 > $soctimerfile
	socDebugLog "Requesting SoC"
	re='^-?[0-9]+$'
	soclevel=$(python3 $MODULEDIR/voc -u $username -p $password dashboard |grep 'Battery level' | cut -f2 -d":" |sed 's/[^0-9]*//g')
	socDebugLog "Answer: $soclevel"
	if  [[ $soclevel =~ $re ]] ; then
		if (( $soclevel != 0 )) ; then
			socDebugLog "Valid SoC found: $soclevel"
			echo $soclevel > $socfile
		fi
	fi

fi
