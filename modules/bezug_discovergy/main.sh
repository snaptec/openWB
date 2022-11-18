#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
#DMOD="EVU"
DMOD="MAIN"

if [ ${DMOD} == "MAIN" ]; then
	MYLOGFILE="${RAMDISKDIR}/openWB.log"
else
	MYLOGFILE="${RAMDISKDIR}/evu.log"
fi

# If both wr_discovergy and bezug_discovergy are activated, then runs/loadvars.sh will run `wr_discovergy` first.
# In this case wr_discovergy will fetch data for both inverter and counter and there is nothing left for us to do
# except reading the `wattbezug` file from ramdisk.
#
# If only bezug_discovery is activated then we fetch counter data here.
#
# The usage of wr_discovergy without bezug_discovergy is not intended and thus not handled.

if [[ "$pvwattmodul" != "wr_discovergy" ]]; then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.devices.discovergy.device" "$discovergyuser" "$discovergypass" "$discovergyevuid" "" >>"$MYLOGFILE" 2>&1
fi

cat "${RAMDISKDIR}/wattbezug"
