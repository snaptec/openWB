#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_vag
$OPENWBBASEDIR/modules/soc_vag/main.sh 2
exit 0
