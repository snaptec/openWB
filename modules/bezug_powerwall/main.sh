#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
Debug=$debug
myPid=$$

sudo python3 /var/www/html/openWB/modules/bezug_powerwall/powerwall.py $OPENWBBASEDIR $Debug $myPid $speicherpwloginneeded $speicherpwuser $speicherpwpass $speicherpwip
wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
echo $wattbezug