#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#MODULEDIR=$(cd `dirname $0` && pwd)
DMOD="PV"
#DMOD="MAIN"
Debug=$debug

#For Development only
#Debug=1

if [ $DMOD == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/nurpv.log"
fi

#bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_shelly.shellywr" "${pv1_ipa}" pvwatt >>$MYLOGFILE 2>&1
#ret=$?

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.shelly.device" "inverter" "$pv1_ipa" "1" >>"$MYLOGFILE" 2>&1
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"

cat "$OPENWBBASEDIR/ramdisk/pvwatt"
