#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_aiways
$OPENWBBASEDIR/modules/soc_aiways/main.sh 2
exit 0
