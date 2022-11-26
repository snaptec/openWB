#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="PV"
#DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.openwb_evu_kit.device" "counter" "${evukitversion}" "${speichermodul}" "${speicherkitversion}" "2" "${pv2wattmodul}" "${pv2kitversion}" >>"$MYLOGFILE" 2>&1
cat "$RAMDISKDIR/pvwatt"
