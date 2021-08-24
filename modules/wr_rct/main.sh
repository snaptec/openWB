#!/bin/bash
#pv1watt und pv1total ist String A
#pv2watt und pv2total ist der externe Bezug
#pv3watt und pv3total ist String B
pv1watt=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xB5317B78')/1" | bc)
pv2watt=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xE96F1844')/1" | bc)
pv3watt=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xAA9AA253')/1" | bc)
pvwatt=$(echo "scale=0; ($pv1watt + $pv2watt + $pv3watt) * -1" | bc)
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvwatt
pv1total=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xFC724A9E')/1" | bc)
pv2total=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xF28E2E1')/1" | bc)
pv3total=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0x68EEFD3D')/1" | bc)
pvtotal=$(echo "scale=0; ($pv1total + $pv2total + $pv3total)" | bc)
echo $pvtotal > /var/www/html/openWB/ramdisk/pvkwh

