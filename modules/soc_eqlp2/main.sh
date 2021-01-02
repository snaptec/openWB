#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_eq
$OPENWBBASEDIR/modules/soc_eq/main.sh 2
exit 0
