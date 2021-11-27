#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MYLOGFILE="$RAMDISKDIR/openWB.log"

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "wr_fronius: Seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
	# load helperFunctions
	. $OPENWBBASEDIR/helperFunctions.sh
fi

python3 /var/www/html/openWB/modules/wr_fronius/fronius.py "${wrfroniusip}" "${wrfronius2ip}" "${wrfroniusisgen24}" &>>$MYLOGFILE

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
