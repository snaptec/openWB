#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_myrenault
$OPENWBBASEDIR/modules/soc_myrenault/main.sh 2
exit 0
