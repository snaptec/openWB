#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
DMOD="MAIN"

#For development only
#Debug=1

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi
if { [[ $pvwattmodul != "wr_ethmpm3pmaevu" ]] || [[ $pv2wattmodul != "wr2_ethlovatoaevu" ]]; } && [[ $speichermodul != "speicher_sdmaevu" ]]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.openwb_evu_kit.device" "counter" "${evukitversion}" >>"$MYLOGFILE" 2>&1
	ret=$?
	openwbDebugLog ${DMOD} 2 "EVU RET: ${ret}"
fi

cat "${RAMDISKDIR}/wattbezug"
