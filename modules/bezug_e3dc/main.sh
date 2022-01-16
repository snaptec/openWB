#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
python3 "$OPENWBBASEDIR/modules/bezug_e3dc/e3dc.py" "$e3dcip"  >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1
cat "$OPENWBBASEDIR/ramdisk/wattbezug"
