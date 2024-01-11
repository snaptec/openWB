#!/bin/bash

OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/wr_kostalpikovar2.log"
fi

urlPattern='^(http[s]?)://'
if ! [[ "${wr_piko2_url}" =~ $urlPattern ]]; then
	wr_piko2_url="http://${wr_piko2_url}"
	openwbDebugLog ${DMOD} 0 "Unvollständige URL! Ergänze 'http://'. -> ${wr_piko2_url}"
fi

openwbDebugLog ${DMOD} 2 "WR User: ${wr_piko2_user}"
openwbDebugLog ${DMOD} 2 "WR Passwort: ${wr_piko2_pass}"
openwbDebugLog ${DMOD} 2 "WR URL: ${wr_piko2_url}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.kostal_piko_old.device" "inverter" "${wr_piko2_url}" "${wr_piko2_user}" "${wr_piko2_pass}" 1 >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pvwatt"
