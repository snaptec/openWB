#!/bin/bash

SOCMODULE="kia"

MODULEDIR=$(cd `dirname $0` && pwd)
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
LOGFILE="$RAMDISKDIR/soc.log"
CHARGEPOINT=$1
DEBUGLEVEL=$debug


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
		abrp_enable=$kia_abrp_enable_2
		abrp_token=$kia_abrp_token_2
		advanced=$kia_advanced2
		adv_cachevalid=$kia_adv_cachevalid2
		adv_12v=$kia_adv_12v2
		adv_interval_unplug=$kia_adv_interval_unplug2
		adv_ratelimit=$kia_adv_ratelimit2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for soclogging)
		CHARGEPOINT=1
		kia_email=$soc_bluelink_email
		kia_password=$soc_bluelink_password
		kia_pin=$soc_bluelink_pin
		kia_vin=$soc_vin
		kia_intervall=$soc_bluelink_interval
		soccalc=$kia_soccalclp1
		akkug=$akkuglp1
		efficiency=$wirkungsgradlp1
		abrp_enable=$kia_abrp_enable
		abrp_token=$kia_abrp_token
		advanced=$kia_advanced
		adv_cachevalid=$kia_adv_cachevalid
		adv_12v=$kia_adv_12v
		adv_interval_unplug=$kia_adv_interval_unplug
		adv_ratelimit=$kia_adv_ratelimit
		;;
esac

ARGSFILE="$RAMDISKDIR/soc_${SOCMODULE}_lp${CHARGEPOINT}_args"

ARGS='{'
ARGS+='"moduleName": "'"$SOCMODULE"'", '
ARGS+='"chargePoint": "'"$CHARGEPOINT"'", '
ARGS+='"accountName": "'"$kia_email"'", '
ARGS+='"accountPassword": "'"$kia_password"'", '
ARGS+='"accountPin": "'"$kia_pin"'", '
ARGS+='"vehicleVin": "'"$kia_vin"'", '
ARGS+='"timerInterval": "'"$kia_intervall"'", '
ARGS+='"manualCalc": "'"$soccalc"'", '
ARGS+='"batterySize": "'"$akkug"'", '
ARGS+='"efficiency": "'"$efficiency"'", '
ARGS+='"abrpEnable": "'"$abrp_enable"'", '
ARGS+='"abrpToken": "'"$abrp_token"'", '
ARGS+='"advEnable": "'"$advanced"'", '
ARGS+='"advCacheValid": "'"$adv_cachevalid"'", '
ARGS+='"adv12vLimit": "'"$adv_12v"'", '
ARGS+='"advIntUnplug": "'"$adv_interval_unplug"'", '
ARGS+='"advRateLimit": "'"$adv_ratelimit"'", '
ARGS+='"ramDiskDir": "'"$RAMDISKDIR"'", '
ARGS+='"debugLevel": "'"$DEBUGLEVEL"'"'
ARGS+='}'

echo $ARGS > $ARGSFILE

sudo python3 $MODULEDIR/main.py $ARGSFILE &>> $LOGFILE &
