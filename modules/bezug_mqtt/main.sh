#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"

cat "${RAMDISKDIR}/wattbezug"

openwbModulePublishState "EVU" 0 "Kein Fehler"
