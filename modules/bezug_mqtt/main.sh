#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)

source $OPENWBBASEDIR/helperFunctions.sh

wattbezug=$(<$RAMDISKDIR/wattbezug)
echo $wattbezug

openwbPublishModuleState "EVU" 0 "Kein Fehler"
