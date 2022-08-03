#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
CHARGEPOINT=${1:-1}

efficiency_var_name=wirkungsgradlp"$CHARGEPOINT"
battery_size_var_name=akkuglp"$CHARGEPOINT"
bash "$OPENWBBASEDIR/packages/legacy_run.sh" "soc_manual.soc_manual" "$CHARGEPOINT" "${!efficiency_var_name}" "${!battery_size_var_name}" >>"$RAMDISKDIR/soc.log" 2>&1
