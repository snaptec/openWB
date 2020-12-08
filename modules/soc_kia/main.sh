#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		kia_email=$soc2user
		kia_password=$soc2pass
		kia_pin=$soc2pin
		kia_vin=$soc2vin
		kia_intervall=$soc2intervall
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		kia_email=$soc_bluelink_email
		kia_password=$soc_bluelink_password
		kia_pin=$soc_bluelink_pin
		kia_vin=$soc_vin
		kia_intervall=$soc_bluelink_interval
		;;
esac

soctimer=$(<$soctimerfile)
tmpintervall=$(( kia_intervall * 6 ))

if (( soctimer < tmpintervall )); then
	soctimer=$((soctimer+1))
	echo $soctimer > soctimerfile
else
	sudo python3 $MODULEDIR/kiasoc.py $kia_email $kia_password $kia_pin $kia_vin $socfile &
	echo 0 > soctimerfile
fi
