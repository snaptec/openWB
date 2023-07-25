#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="$RAMDISKDIR/openWB.log"
else
	MYLOGFILE="$RAMDISKDIR/bezug_solarlog.log"
fi

openwbDebugLog ${DMOD} 2 "Bezug Solarlog IP: ${bezug_solarlog_ip}"
openwbDebugLog ${DMOD} 2 "Bezug Solarlog Speicher : ${bezug_solarlog_speicherv}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.solar_log.device" "counter" "${bezug_solarlog_ip}" "${bezug_solarlog_speicherv}" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "${RAMDISKDIR}/wattbezug"
