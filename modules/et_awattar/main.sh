#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "et_awattar: seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. $OPENWBBASEDIR/loadconfig.sh
fi

# abort if we try to use unset variables
set -o nounset

# call module with parameters: location = at or de and baseprice (only for Germany, 0 if not set)
sudo python3 /var/www/html/openWB/modules/et_awattar/awattargetprices.py $awattarlocation 0 $debug
