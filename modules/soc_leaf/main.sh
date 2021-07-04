#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="EVSOC"
CHARGEPOINT=$1

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "soc_leaf: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

case $CHARGEPOINT in
	2)
		# second charge point
		username=$leafusernames1
		password=$leafpassworts1
		;;
	*)
		# defaults to first charge point for backward compatibility
		# set CHARGEPOINT in case it is empty (needed for logging)
		CHARGEPOINT=1
		username=$leafusername
		password=$leafpasswort
		;;
esac

openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Starting Python module"
sudo python /var/www/html/openWB/modules/soc_leaf/soc.py $username $password $CHARGEPOINT
openwbDebugLog ${DMOD} 1 "Lp$CHARGEPOINT: Done"
