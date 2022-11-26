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

if [ "${wattbezugmodul}" = "bezug_huawei" ]; then
	READ_COUNTER="True"
else
	READ_COUNTER="False"
fi
if [ "${speichermodul}" = "speicher_huawei" ]; then
	READ_BATTERY="True"
else
	READ_BATTERY="False"
fi

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.huawei.device" "${pv1_ipa}" "${pv1_ida}" "$READ_COUNTER" "$READ_BATTERY" >>"$MYLOGFILE" 2>&1

cat "${RAMDISKDIR}/pvwatt"
