#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_citogo: Seems like openwb.conf is not loaded. Reading file."
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
		username=$soc2user
		password=$soc2pass
		intervall=$((60 * 6))
		intervallladen=$((10 * 6))
		opts=$soc2opts
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		ladeleistung=$(<$RAMDISKDIR/llaktuell)
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		username=$socuser
		password=$socpass
		intervall=$((60 * 6))
		intervallladen=$((10 * 6))
		opts=$socopts
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
#	openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Requesting SoC [debug:$debug] $opts "
	echo 0 > $soctimerfile

    start=`date +%s`
	$MODULEDIR/callskoda.py -u $username -p $password -l $CHARGEPOINT -d $debug $opts



    end=`date +%s`
	runtime=$((end-start))
	openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Requesting SkodaConnect SoC, runtime: $runtime Sec. [debug:$debug] "

    if [ -f /var/www/html/openWB/ramdisk/carinfo_* ] ; then
      chown pi:pi /var/www/html/openWB/ramdisk/carinfo_*
    fi

    
# Nicht noetig, callskoda trage die Werte direkt in MQTT ein
#	if [ $? -eq 0 ]; then
#		# we got a valid answer
#		echo $answer > $socfile
#		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: SoC: $answer"
#	else
#		# we have a problem
#		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Error from EVCC: $answer"
#	fi

}
if [ "$username" == "" ] ; then
  openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: No User, no aktion"
  exit 1
fi
if [ "$password" == "" ] ; then
  openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: No Passowrd, no aktion"
  exit 2
fi


soctimer=$(<$soctimerfile)
# openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: timer = $soctimer"
if (( ladeleistung > 500 )); then
	if (( soctimer < intervallladen )); then
		incrementTimer
		openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Charging, but nothing to do yet. Incrementing timer to $soctimer from $intervallladen"
	else
		getAndWriteSoc
	fi
else
	if (( soctimer < intervall )); then
		incrementTimer
		# openwbDebugLog ${DMOD} 0 "Lp$CHARGEPOINT: Nothing to do yet. Incrementing timer to $soctimer from $intervall."
	else
		getAndWriteSoc
	fi
fi


