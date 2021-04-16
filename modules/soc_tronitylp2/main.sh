#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_tronity
$OPENWBBASEDIR/modules/soc_tronity/main.sh 2
exit 0
