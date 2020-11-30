#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_mypeugeot
$OPENWBBASEDIR/modules/soc_mypeugeot/main.sh 2
exit 0
