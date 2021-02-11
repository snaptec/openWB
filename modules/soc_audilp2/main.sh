#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_audi
$OPENWBBASEDIR/modules/soc_audi/main.sh 2
exit 0
