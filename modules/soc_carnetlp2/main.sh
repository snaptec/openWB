#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_carnet
$OPENWBBASEDIR/modules/soc_carnet/main.sh 2
exit 0
