#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_id
$OPENWBBASEDIR/modules/soc_id/main.sh 2
exit 0
