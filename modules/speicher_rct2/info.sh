#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)
CONFIGFILE="$OPENWBBASEDIR/openwb.conf"


# Call readmodule from bezug_rct2    
python /var/www/html/openWB/modules/bezug_rct2/rct_read_speicher_info.py $opt --ip=$bezug1_ip  


