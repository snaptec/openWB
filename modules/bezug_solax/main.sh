#!/bin/bash

python /var/www/html/openWB/modules/bezug_solax/solax.py $solaxip

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
