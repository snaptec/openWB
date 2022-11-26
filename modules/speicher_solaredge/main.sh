#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="BAT"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/bat.log"
fi

if [[ "$solaredgespeicherip" == "$solaredgepvip" ]]; then
	echo "value read at pv modul" >/dev/null
else
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solaredge.device" "bat" "$solaredgespeicherip" "" "1" "2" "none" "none" "0" "0" "$solaredgezweiterspeicher" >>"$MYLOGFILE" 2>&1
	ret=$?
fi

openwbDebugLog ${DMOD} 2 "BAT RET: ${ret}"
