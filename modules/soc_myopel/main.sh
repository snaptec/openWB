#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		username=$myopel_userlp2
		password=$myopel_passlp2
		clientId=$myopel_clientidlp2
		clientSecret=$myopel_clientsecretlp2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		username=$myopel_userlp1
		password=$myopel_passlp1
		clientId=$myopel_clientidlp1
		clientSecret=$myopel_clientsecretlp1
		;;
esac

timer=$(<$soctimerfile)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > $soctimerfile
else
	sudo python $MODULEDIR/opelsoc.py $CHARGEPOINT $username $password $clientId $clientSecret
	echo 0 > $soctimerfile
fi
