#!/bin/bash
soc=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --name='battery.soc')*100/1" | bc)
echo $soc > /var/www/html/openWB/ramdisk/speichersoc
watt=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --name='g_sync.p_acc_lp')*-1/1" | bc)
echo $watt > /var/www/html/openWB/ramdisk/speicherleistung