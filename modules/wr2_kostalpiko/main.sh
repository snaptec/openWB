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
openwbDebugLog ${DMOD} 2 "WR IP: ${pv2ip}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" 1 "wr_kostalpiko.kostal_piko_var1" 2 "${speichermodul}" "${pv2ip}" >>"${MYLOGFILE}" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt) 
echo "$pvwatt"
