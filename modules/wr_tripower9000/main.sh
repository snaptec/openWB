#!/bin/bash

python3 /var/www/html/openWB/modules/wr_tripower9000/tripower.py "${wrsmawebbox}" "${tri9000ip}" "${wrsma2ip}" "${wrsma3ip}" "${wrsma4ip}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
ekwh=$(</var/www/html/openWB/ramdisk/pvkwh)
pvkwhk=$(echo "scale=3;$ekwh / 1000" |bc)
echo $pvkwhk > /var/www/html/openWB/ramdisk/pvkwhk
