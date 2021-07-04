#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_kia
$OPENWBBASEDIR/modules/soc_kia/main.sh 1
exit 0
