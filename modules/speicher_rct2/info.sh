#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"

# check if config file is already in env
if [[ -z "$debug" ]]; then
	. $OPENWBBASEDIR/loadconfig.sh
fi


# Call readmodule from bezug_rct2    
timeout -k 9 3 python3 /var/www/html/openWB/modules/bezug_rct2/rct_read_speicher_info.py --ip=$bezug1_ip
rc=$?
if  [[ ($rc == 143)  || ($rc == 124) ]] ; then
  echo "Speicher-Info Script timed out"
fi
exit $rc
