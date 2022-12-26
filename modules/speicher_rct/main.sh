#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)
DMOD="MAIN"

openwbDebugLog ${DMOD} 2 "RCT Bat start"

soc=$(echo "scale=0; $(python "${MODULEDIR}/../bezug_rct/rct_read.py" --ip="$bezug1_ip" --name='battery.soc')*100/1" | bc)
echo "$soc" > "$RAMDISKDIR/speichersoc"
openwbDebugLog ${DMOD} 2 "RCT Bat soc: $soc"

watt=$(echo "scale=0; $(python "${MODULEDIR}/../bezug_rct/rct_read.py" --ip="$bezug1_ip" --name='g_sync.p_acc_lp')*-1/1" | bc)
echo "$watt" > "$RAMDISKDIR/speicherleistung"
openwbDebugLog ${DMOD} 2 "RCT Bat power: $watt"
