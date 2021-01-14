#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_i3
$OPENWBBASEDIR/modules/soc_i3/main.sh 2
exit 0
