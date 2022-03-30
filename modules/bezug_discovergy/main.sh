#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# If both wr_discovergy and bezug_discovergy are activated, then runs/loadvars.sh will run `wr_discovergy` first.
# In this case that wr_discovergy will fetch data for both inverter end counter and there is nothing left for us to do
# except reading the `wattbezug` file from ramdisk.
#
# If only bezug_discovery is activated then we fetch counter data here.
#
# The usage of wr_discovergy without bezug_discovergy is not intended and thus not handled.

if [[ "$pvwattmodul" != "wr_discovergy" ]]
then
	bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.discovergy.device" "$discovergyuser" "$discovergypass" "$discovergyevuid" "" >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1
fi

cat /var/www/html/openWB/ramdisk/wattbezug
