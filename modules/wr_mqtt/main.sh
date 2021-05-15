#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)

pvwatt=$(<$RAMDISKDIR/pvwatt)
echo $pvwatt

openwbModulePublishState "PV" 0 "Kein Fehler" 1
