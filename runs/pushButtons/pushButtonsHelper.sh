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

pushButtonsStart() {
	if pgrep -f '^python.*/pushButtonsDaemon.py' >/dev/null; then
		openwbDebugLog "MAIN" 2 "push buttons handler already running"
	else
		openwbDebugLog "MAIN" 1 "push buttons handler not running! starting process"
		python3 "$OPENWBBASEDIR/runs/pushButtons/pushButtonsDaemon.py" >>"$RAMDISKDIR/openWB.log" 2>&1 &
	fi
}

pushButtonsStop() {
	if pgrep -f '^python.*/pushButtonsDaemon.py' >/dev/null; then
		openwbDebugLog "MAIN" 1 "push buttons handler running but not configured. killing handler"
		sudo pkill -f '^python.*/pushButtonsDaemon.py'
	fi
}

pushButtonsSetup() {
	local enabled=$1
	local forceRestart=$2

	if ((forceRestart == 1)); then
		openwbDebugLog "MAIN" 2 "push buttons handler restart forced! killing handler"
		pushButtonsStop
	fi
	if ((enabled == 1)); then
		openwbDebugLog "MAIN" 1 "push buttons enabled"
		pushButtonsStart
	else
		openwbDebugLog "MAIN" 1 "push buttons disabled"
		pushButtonsStop
	fi
}
export -f pushButtonsSetup
