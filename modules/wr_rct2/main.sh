#!/bin/bash

# Call readmodule from bezug_rct2    
python3 /var/www/html/openWB/modules/bezug_rct2/rct_read_wr.py --ip=$bezug1_ip 

#
# return a value to loadvars.sh
#
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
