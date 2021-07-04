#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_zoe
$OPENWBBASEDIR/modules/soc_zoe/main.sh 2
exit 0
