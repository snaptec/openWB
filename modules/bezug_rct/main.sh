#!/bin/bash
ampere1=$(echo "scale=1; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0x27BE51D9')/230/1" | bc)
ampere2=$(echo "scale=1; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xF5584F90')/230/1" | bc)
ampere3=$(echo "scale=1; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xB221BCFA')/230/1" | bc)
echo $ampere1 > /var/www/html/openWB/ramdisk/bezuga1
echo $ampere2 > /var/www/html/openWB/ramdisk/bezuga2
echo $ampere3 > /var/www/html/openWB/ramdisk/bezuga3

wattbezug=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0x6002891F')/1" | bc)
watt1=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0x27BE51D9')/1" | bc)
watt2=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xF5584F90')/1" | bc)
watt3=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xB221BCFA')/1" | bc)
echo $watt1 > /var/www/html/openWB/ramdisk/bezugw1
echo $watt2 > /var/www/html/openWB/ramdisk/bezugw2
echo $watt3 > /var/www/html/openWB/ramdisk/bezugw3

echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $wattbezug

