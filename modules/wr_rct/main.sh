#!/bin/bash
pv1watt=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xB5317B78')/1" | bc)
pv2watt=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xE96F1844')/1" | bc)
pv3watt=$(echo "scale=0; $(python /var/www/html/openWB/modules/bezug_rct/rct_read.py --ip=$bezug1_ip --id='0xAA9AA253')/1" | bc)
pvwatt=$(echo "scale=0; ($pv1watt + $pv2watt + $pv3watt) * -1" | bc)
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvwatt
