#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

bash "$OPENWBBASEDIR/packages/legacy_run.sh" "modules.discovergy.device" "$discovergyuser" "$discovergypass" "$discovergyevuid" "$discovergypvid" &>> "$OPENWBBASEDIR/ramdisk/openWB.log"

cat "$OPENWBBASEDIR/ramdisk/pvwatt"
