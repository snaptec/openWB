#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
timeout 3 python3 "$OPENWBBASEDIR/modules/bezug_smashm/sma_em_measurement.py" "$smashmbezugid" >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1
cat /var/www/html/openWB/ramdisk/wattbezug
