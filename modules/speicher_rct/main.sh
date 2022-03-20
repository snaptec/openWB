#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"
MODULEDIR=$(cd "$(dirname "$0")" && pwd)

soc=$(echo "scale=0; $(python "${MODULEDIR}/../bezug_rct/rct_read.py" --ip="$bezug1_ip" --name='battery.soc')*100/1" | bc)
echo "$soc" > "$RAMDISKDIR/speichersoc"
watt=$(echo "scale=0; $(python "${MODULEDIR}/../bezug_rct/rct_read.py" --ip="$bezug1_ip" --name='g_sync.p_acc_lp')*-1/1" | bc)
echo "$watt" > "$RAMDISKDIR/speicherleistung"
