#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_tesla
$OPENWBBASEDIR/modules/soc_tesla/main.sh 2
exit 0
