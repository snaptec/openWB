#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_kostalpico.log"
fi

openwbDebugLog ${DMOD} 2 "WR Speicher: ${speichermodul}"
openwbDebugLog ${DMOD} 2 "WR IP: ${wrkostalpikoip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.kostal_piko.device" "inverter" "${wrkostalpikoip}" "${speichermodul}" "${bydhvip}" "${bydhvuser}" "${bydhvpass}" 1 >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
cat "$RAMDISKDIR/pvwatt"
