#!/bin/bash
if [[ -z "$OPENWBBASEDIR" ]]; then
	OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
fi
if [[ -z "$RAMDISKDIR" ]]; then
	RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
fi

declare -F openwbDebugLog &>/dev/null || {
	. "$OPENWBBASEDIR/helperFunctions.sh"
}

remoteSupportStart() {
	if pgrep -f '^python.*/remoteSupport.py' >/dev/null; then
		openwbDebugLog "MAIN" 2 "remote support handler already running"
	else
		openwbDebugLog "MAIN" 1 "remote support handler not running! starting process"
		python3 "$OPENWBBASEDIR/runs/remoteSupport/remoteSupport.py" >>"$RAMDISKDIR/openWB.log" 2>&1 &
	fi
}

remoteSupportStop() {
	if pgrep -f '^python.*/remoteSupport.py' >/dev/null; then
		openwbDebugLog "MAIN" 1 "remote support handler running but stop requested. killing handler"
		sudo pkill -f '^python.*/remoteSupport.py'
	fi
}

remoteSupportSetup() {
	local forceRestart=$1

	if ((forceRestart == 1)); then
		openwbDebugLog "MAIN" 2 "remote support handler restart forced! killing handler"
		remoteSupportStop
	fi
	openwbDebugLog "MAIN" 1 "starting remote support handler"
	remoteSupportStart
}
export -f remoteSupportSetup
