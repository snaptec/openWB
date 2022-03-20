#!/bin/bash

if [ -n "$bezug1_ip" ]; then
	  opt=""
  else
	    echo "$0 Debughilfe bezug1_ip parameter not supplied use 192.168.208.63"
	      bezug1_ip=192.168.208.63
	        # opt=" -v"
		  opt=""     # Kein echo!
	  fi

# Call readmodule from bezug_rct2    
python3 /var/www/html/openWB/modules/bezug_rct2/rct_read_wr.py --ip=$bezug1_ip 

#
# return a value to loadvars.sh
#
pvwatt=$(</var/www/html/openWB/ramdisk/pvwatt)
echo $pvwatt
