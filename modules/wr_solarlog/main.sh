#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname $0)/../../" && pwd)
MODULEDIR=$(cd "$(dirname $0)" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MYLOGFILE="${RAMDISKDIR}/nurpv.log"

DMOD="PV"
Debug=$debug

python3 "${MODULEDIR}/solarlog.py" "${bezug_solarlog_ip}" >> "${MYLOGFILE}" 2>&1
pvwatt=$(<"${RAMDISKDIR}/pvwatt")
pvkwh=$(<"${RAMDISKDIR}/pvkwh")

openwbDebugLog ${DMOD} 2 "pvwatt: $pvwatt"
openwbDebugLog ${DMOD} 2 "pvkwh: $pvkwh"
echo $pvwatt
