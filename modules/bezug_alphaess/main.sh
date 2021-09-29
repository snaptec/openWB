#!/bin/bash

python3 /var/www/html/openWB/packages/modules/counter/alpha_ess.py "${alphav123}"

wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug
