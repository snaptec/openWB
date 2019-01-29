#!/bin/bash
. /var/www/html/openWB/openwb.conf



sudo python /var/www/html/openWB/modules/wr_tripower9000/tri9000.py $tri9000ip


pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
ekwh=$(</var/www/html/openWB/ramdisk/pvkwh)


pvkwhk=$(echo "scale=3;$ekwh / 1000" |bc)
echo $pvkwhk > ramdisk/pvkwhk





