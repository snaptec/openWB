#!/bin/bash
OPENWBBASEDIR=$(cd "$(dirname "$0")/../../" && pwd)
RAMDISKDIR="${OPENWBBASEDIR}/ramdisk"

output=$(curl --connect-timeout 3 -s -u "$powerfoxuser":"$powerfoxpass" "https://backend.powerfox.energy/api/2.0/my/$powerfoxpvid/current")

pvwh=$(echo "$output" | jq '.A_Plus')
echo "$pvwh" > "$RAMDISKDIR/pvkwh"

watt=$(echo "$output" | jq '.Watt')
echo "$watt" > "$RAMDISKDIR/pvwatt"

echo "$watt"
