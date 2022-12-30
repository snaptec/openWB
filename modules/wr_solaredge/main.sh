#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
#DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

Solaredgebatwr="0"
if [[ "$solaredgespeicherip" == "$solaredgepvip" ]]; then
	Solaredgebatwr="1"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solaredge.device" "inverter" "$solaredgepvip" "" "$solaredgepvslave1" "$solaredgepvslave2" "$solaredgepvslave3" "$solaredgepvslave4" "$Solaredgebatwr" "$wr1extprod" "$solaredgezweiterspeicher" "$solaredgesubbat" "$solaredgewr2ip" "1" >>"$MYLOGFILE" 2>&1
ret=$?
openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
