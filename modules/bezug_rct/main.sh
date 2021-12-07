#!/bin/bash

wattbezug=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --name='g_sync.p_ac_sc_sum')/1" | bc)
watt1=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0x27BE51D9')/230/1" | bc)
watt2=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xF5584F90')/230/1" | bc)
watt3=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xB221BCFA')/230/1" | bc)
echo $watt1 > /var/www/html/openWB/ramdisk/bezuga1
echo $watt2 > /var/www/html/openWB/ramdisk/bezuga2
echo $watt3 > /var/www/html/openWB/ramdisk/bezuga3

echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $wattbezug
