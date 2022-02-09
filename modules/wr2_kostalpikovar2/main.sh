#!/bin/bash

python3 /var/www/html/openWB/modules/wr_kostalpikovar2/kostal_piko_var2.py 2 $wr2_piko2_url $wr2_piko2_user $wr2_piko2_pass
pvwatt=$(</var/www/html/openWB/ramdisk/pv2watt) 
echo $pvwatt