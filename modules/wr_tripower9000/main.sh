#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

python3 /var/www/html/openWB/modules/wr_tripower9000/tripower.py "${wrsmawebbox}" "${tri9000ip}" "${wrsma2ip}" "${wrsma3ip}" "${wrsma4ip}" >> "$OPENWBBASEDIR/ramdisk/openWB.log" 2>&1
cat /var/www/html/openWB/ramdisk/pvwatt
