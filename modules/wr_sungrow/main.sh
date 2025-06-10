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

if [[ "$wattbezugmodul" == "bezug_sungrow" ]]; then
	read_counter=1
else
	read_counter=0
fi
bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.sungrow.device" "inverter" "$speicher1_ip" "$sungrowspeicherport" "$sungrowspeicherid" "1" "$read_counter" "$sungrowsr" >>"$MYLOGFILE" 2>&1

cat "$RAMDISKDIR/pvwatt"
