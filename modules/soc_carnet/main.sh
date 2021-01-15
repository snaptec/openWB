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
		soctimerfile="$RAMDISKDIR/soctimer1"
		socfile="$RAMDISKDIR/soc1"
		intervall=$soccarnetlp2intervall
		username=$carnetlp2user
		password=$carnetlp2pass
		;;
	*)
		# defaults to first charge point for backward compatibility
		soctimerfile="$RAMDISKDIR/soctimer"
		socfile="$RAMDISKDIR/soc"
		intervall=$soccarnetintervall
		username=$carnetuser
		password=$carnetpass
		;;
esac

vwtimer=$(<$soctimerfile)
if (( vwtimer < 60 )); then
	vwtimer=$((vwtimer+1))
	echo $vwtimer > $soctimerfile
else
	echo 0 > $soctimerfile
	/var/www/html/openWB/modules/soc_carnet/soc.sh $username $password
	#Abfrage Ladung aktiv. Setzen des soctimers. 
	if (( ladeleistung > 800 )) ; then
		vwtimer=$((60 * (10 - $intervall) / 10))
		echo $vwtimer > $soctimerfile
	fi
	
	/var/www/html/openWB/modules/soc_carnet/soc.sh $username $password $socfile
fi
