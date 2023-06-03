#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/evu.log"
fi

if [[ "$pvwattmodul" == "wr_sungrow" ]]; then
	echo "value read at pv modul" >/dev/null
else
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.sungrow.device" "counter" "$pv1_ipa" "$pv1_ida" "$sungrowsr" >>"$MYLOGFILE" 2>&1
	ret=$?
fi

openwbDebugLog $DMOD 2 "EVU RET: $ret"

cat "${RAMDISKDIR}/wattbezug"
