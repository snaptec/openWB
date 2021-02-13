#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "et_tibber: seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
fi

# abort if we try to use unset variables
set -o nounset

sudo python3 /var/www/html/openWB/modules/et_tibber/tibbergetprices.py $tibbertoken $tibberhomeid $debug
