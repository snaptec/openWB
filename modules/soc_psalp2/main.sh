#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_psa
$OPENWBBASEDIR/modules/soc_psa/main.sh 2
exit 0
