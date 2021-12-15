#!/bin/bash

python3 /var/www/html/openWB/modules/wr_tripower9000/tripower.py "${wrsmawebbox}" "${tri9000ip}" "${wrsma2ip}" "${wrsma3ip}" "${wrsma4ip}"
cat /var/www/html/openWB/ramdisk/pvwatt
