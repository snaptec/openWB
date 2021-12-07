#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_manual
$OPENWBBASEDIR/modules/soc_manual/main.sh 2
exit 0
