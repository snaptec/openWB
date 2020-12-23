#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_bluelink
$OPENWBBASEDIR/modules/soc_bluelink/main.sh 2
exit 0
