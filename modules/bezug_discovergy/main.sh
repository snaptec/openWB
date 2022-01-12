#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

python3 /var/www/html/openWB/modules/bezug_discovergy/discovergy.py "$discovergyuser" "$discovergypass" "$discovergyevuid" &>> "$OPENWBBASEDIR/ramdisk/openWB.log"
cat /var/www/html/openWB/ramdisk/wattbezug
