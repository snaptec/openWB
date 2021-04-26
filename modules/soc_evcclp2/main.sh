#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_evcc
$OPENWBBASEDIR/modules/soc_evcc/main.sh 2
exit 0
