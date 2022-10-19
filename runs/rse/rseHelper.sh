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

rseStart() {
	if pgrep -f '^python.*/rseDaemon.py' >/dev/null; then
		openwbDebugLog "MAIN" 2 "rse handler already running"
	else
		openwbDebugLog "MAIN" 1 "rse handler not running! starting process"
		python3 "$OPENWBBASEDIR/runs/rse/rseDaemon.py" >>"$RAMDISKDIR/openWB.log" 2>&1 &
	fi
}

rseStop() {
	if pgrep -f '^python.*/rseDaemon.py' >/dev/null; then
		openwbDebugLog "MAIN" 1 "rse handler running but not configured. killing handler"
		sudo pkill -f '^python.*/rseDaemon.py'
	fi
}

rseSetup() {
	local enabled=$1
	local forceRestart=$2

	if ((forceRestart == 1)); then
		openwbDebugLog "MAIN" 2 "rse handler restart forced! killing handler"
		rseStop
	fi
	if ((enabled == 1)); then
		openwbDebugLog "MAIN" 1 "rse enabled"
		rseStart
	else
		openwbDebugLog "MAIN" 1 "rse disabled"
		rseStop
	fi
}
export -f rseSetup
