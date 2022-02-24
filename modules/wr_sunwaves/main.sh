#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="PV"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_sunwaves.log"
fi

openwbDebugLog ${DMOD} 2 "PV IP: ${wrsunwavesip}"
openwbDebugLog ${DMOD} 2 "PV Passwort: ${wrsunwavespw}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_sunwaves.sunwaves" "${wrsunwavesip}" "${wrsunwavespw}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
