#!/bin/bash
bash "$OPENWBBASEDIR/packages/legacy_run.sh" "wr_shelly.shellywr" "$pv2ip" "pv2watt"
ret=$?

openwbDebugLog ${DMOD} 2 "RET: ${ret}"
pvwatt2=$(</var/www/html/openWB/ramdisk/pv2watt)
echo $pvwatt2
