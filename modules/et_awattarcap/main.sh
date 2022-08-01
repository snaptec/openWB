#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
MODULEDIR=$(cd "$(dirname "$0")" && pwd)

# check if config file is already in env
if [[ -z "$debug" ]]; then
	echo "et_awattar: seems like openwb.conf is not loaded. Reading file."
	# try to load config
	. "$OPENWBBASEDIR/loadconfig.sh"
fi

# abort if we try to use unset variables
set -o nounset

# call module
sudo python3 "$MODULEDIR/awattarcapgetprices.py" "$debug"
