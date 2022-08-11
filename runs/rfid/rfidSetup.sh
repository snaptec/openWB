#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
# try to load config
. "$OPENWBBASEDIR/loadconfig.sh"
# load helperFunctions
. "$OPENWBBASEDIR/helperFunctions.sh"
# load rfidHelper
. "$OPENWBBASEDIR/runs/rfid/rfidHelper.sh"

rfidSetup "$rfidakt" 0 "$rfidlist"
