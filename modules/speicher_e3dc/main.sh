#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
python3 "$OPENWBBASEDIR/modules/speicher_e3dc/e3dc.py" "$e3dcip" "$e3dc2ip" "$e3dcextprod" "$pvwattmodul" >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1
