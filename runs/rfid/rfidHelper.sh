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

rfidInputHandlerStart() {

	# daemon for input0
	if [[ -r /dev/input/event0 ]]; then
		if pgrep -f '^python.*/readrfid.py -d event0' >/dev/null; then
			openwbDebugLog "MAIN" 2 "rfid configured and handler for event0 is running"
		else
			openwbDebugLog "MAIN" 1 "rfid configured but handler for event0 not running; starting process"
			sudo python3 "$OPENWBBASEDIR/runs/rfid/readrfid.py" -d event0 &
		fi
	fi

	# daemon for input1
	if [[ -r /dev/input/event1 ]]; then
		if pgrep -f '^python.*/readrfid.py -d event1' >/dev/null; then
			openwbDebugLog "MAIN" 2 "rfid configured and handler for event1 is running"
		else
			openwbDebugLog "MAIN" 1 "rfid configured but handler for event1 not running; starting process"
			sudo python3 "$OPENWBBASEDIR/runs/rfid/readrfid.py" -d event1 &
		fi
	fi
}
export -f rfidInputHandlerStart

rfidInputHandlerStop() {
	sudo pkill -f '^python.*/readrfid.py'
}
export -f rfidInputHandlerStop

rfidMode2Start() {
	if pgrep -f '^python.*/rfidDaemon.py' >/dev/null; then
		openwbDebugLog "MAIN" 2 "rfid handler already running"
	else
		openwbDebugLog "MAIN" 1 "rfid handler not running! starting process"
		python3 "$OPENWBBASEDIR/runs/rfid/rfidDaemon.py" &
	fi
}
export -f rfidMode2Start

rfidMode2UpdateList() {
	echo "$1" >"$RAMDISKDIR/rfidlist"
}
export -f rfidMode2UpdateList

rfidMode2Stop() {
	sudo pkill -f '^python.*/rfidDaemon.py'
}
export -f rfidMode2Stop

rfidSetup() {
	local mode=$1
	local forceRestart=$2
	local tagList=$3

	if ((forceRestart == 1)); then
		openwbDebugLog "MAIN" 2 "rfid handler restart forced! killing daemons"
		rfidMode2Stop
		rfidInputHandlerStop
	fi
	if ((mode == 0)); then
		rfidMode2Stop
		rfidInputHandlerStop
	else
		rfidInputHandlerStart
	fi
	if ((mode == 2)); then
		rfidMode2UpdateList "$tagList"
		rfidMode2Start
	else
		rfidMode2Stop
	fi
}
export -f rfidSetup
