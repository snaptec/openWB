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
if ! [[ "${wr2_piko2_url}" =~ $urlPattern ]]; then
	wr2_piko2_url="http://${wr2_piko2_url}"
	openwbDebugLog ${DMOD} 0 "Unvollständige URL! Ergänze 'http://'. -> ${wr2_piko2_url}"
fi

openwbDebugLog ${DMOD} 2 "WR User: ${wr2_piko2_user}"
openwbDebugLog ${DMOD} 2 "WR Passwort: ${wr2_piko2_pass}"
openwbDebugLog ${DMOD} 2 "WR URL: ${wr2_piko2_url}"

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.kostal_piko_old.device" "inverter" "${wr2_piko2_url}" "${wr2_piko2_user}" "${wr2_piko2_pass}" 2 >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$RAMDISKDIR/pv2watt"
