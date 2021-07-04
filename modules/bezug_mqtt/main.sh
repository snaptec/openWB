#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)

wattbezug=$(<$RAMDISKDIR/wattbezug)
echo $wattbezug

openwbModulePublishState "EVU" 0 "Kein Fehler"
