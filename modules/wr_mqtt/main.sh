#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)

source $OPENWBBASEDIR/helperFunctions.sh

pvwatt=$(<$RAMDISKDIR/pvwatt)
echo $pvwatt

openwbPublishModuleState "PV" 0 "Kein Fehler" 1
