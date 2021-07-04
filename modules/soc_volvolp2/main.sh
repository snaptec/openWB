#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_volvo
$OPENWBBASEDIR/modules/soc_volvo/main.sh 2
exit 0
