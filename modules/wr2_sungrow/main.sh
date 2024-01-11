#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
DMOD="PV"
#DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/nurpv.log"
fi
read_counter=0

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.sungrow.device" "inverter" "$pv2ip" "$pv2id" "2" "$read_counter" "$sungrow2sr" >>"$MYLOGFILE" 2>&1

cat "$RAMDISKDIR/pv2watt"
