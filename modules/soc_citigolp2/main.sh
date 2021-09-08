#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_citigo
$OPENWBBASEDIR/modules/soc_citigo/main.sh 2
exit 0
