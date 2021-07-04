#!/bin/bash

MODULEDIR=$(cd `dirname $0` && pwd)
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1
socDebug=$debug


case $CHARGEPOINT in
	2)
		# second charge point
		kia_email=$soc2user
		kia_password=$soc2pass
		kia_pin=$soc2pin
		kia_vin=$soc2vin
		kia_intervall=$soc2intervall
		soccalc=$kia_soccalclp2
		akkug=$akkuglp2
		efficiency=$wirkungsgradlp2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		kia_email=$soc_bluelink_email
		kia_password=$soc_bluelink_password
		kia_pin=$soc_bluelink_pin
		kia_vin=$soc_vin
		kia_intervall=$soc_bluelink_interval
		soccalc=$kia_soccalclp1
		akkug=$akkuglp1
		efficiency=$wirkungsgradlp1
		;;
esac

ARGSFILE="$RAMDISKDIR/soc_kia_lp${CHARGEPOINT}_args"
ARGS='{'
ARGS+='"chargePoint": "'"$CHARGEPOINT"'", '
ARGS+='"accountName": "'"$kia_email"'", '
ARGS+='"accountPassword": "'"$kia_password"'", '
ARGS+='"accountPin": "'"$kia_pin"'", '
ARGS+='"vehicleVin": "'"$kia_vin"'", '
ARGS+='"timerInterval": "'"$kia_intervall"'", '
ARGS+='"manualCalc": "'"$soccalc"'", '
ARGS+='"batterySize": "'"$akkug"'", '
ARGS+='"efficiency": "'"$efficiency"'", '
ARGS+='"ramDiskDir": "'"$RAMDISKDIR"'", '
ARGS+='"moduleDir": "'"$MODULEDIR"'", '
ARGS+='"debugLevel": "'"$socDebug"'"'
ARGS+='}'
echo $ARGS > $ARGSFILE
sudo python3 $MODULEDIR/kiasoc.py $ARGSFILE &>> $LOGFILE &
