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

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.sungrow.device" "inverter" "$speicher1_ip" "$sungrowspeicherport" "$sungrowspeicherid" "1">>"$MYLOGFILE" 2>&1

cat "$RAMDISKDIR/pvwatt"
