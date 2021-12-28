#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
python3 "$OPENWBBASEDIR/modules/bezug_solaredge/solaredge.py" "$solaredgeip" "$solaredgemodbusport" "$solaredgepvslave1" >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1
cat "$OPENWBBASEDIR/ramdisk/wattbezug"
