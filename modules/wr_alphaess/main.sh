#!/bin/bash

sudo python3 /var/www/html/openWB/packages/modules/pv/alpha_ess.py "${alphav123}"

pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt