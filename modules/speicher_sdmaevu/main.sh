#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="MAIN"

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/bat.log"
fi

if [[ $pvwattmodul != "wr_ethmpm3pmaevu" ]] || [[ $pv2wattmodul != "wr2_ethlovatoaevu" ]]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.openwb_evu_kit.device" "counter" "${evukitversion}" "${speichermodul}" "${speicherkitversion}" >>"$MYLOGFILE" 2>&1
	ret=$?
fi

openwbDebugLog ${DMOD} 2 "BAT RET: ${ret}"
