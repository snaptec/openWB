#!/bin/bash
#all handled in loadvars.sh & mqttsub.py
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)

openwbModulePublishState "LP" 0 "Kein Fehler" 2
