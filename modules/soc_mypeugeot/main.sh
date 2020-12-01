#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CHARGEPOINT=$1

case $CHARGEPOINT in
	2)
		# second charge point
		soctimerfile="$RAMDISKDIR/soctimer1"
		username=$mypeugeot_userlp2
		password=$mypeugeot_passlp2
		clientId=$mypeugeot_clientidlp2
		clientSecret=$mypeugeot_clientsecretlp2
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		soctimerfile="$RAMDISKDIR/soctimer"
		username=$mypeugeot_userlp1
		password=$mypeugeot_passlp1
		clientId=$mypeugeot_clientidlp1
		clientSecret=$mypeugeot_clientsecretlp1
		;;
esac

timer=$(<$soctimerfile)
if (( timer < 60 )); then
	timer=$((timer+1))
	echo $timer > $soctimerfile
else
	sudo python $MODULEDIR/peugeotsoc.py $CHARGEPOINT $username $password $clientId $clientSecret
	echo 0 > $soctimerfile
fi
