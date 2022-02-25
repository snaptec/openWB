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

bash "$OPENWBBASEDIR/packages/legacy_run.sh" 1 "wr_kostalpiko.kostal_piko_var1" "${speichermodul}" "${wrkostalpikoip}" >>"${MYLOGFILE}" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
pvwatt=$(<"$RAMDISKDIR/pvwatt")
echo "$pvwatt"
