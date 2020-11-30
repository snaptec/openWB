#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_myopel
$OPENWBBASEDIR/modules/soc_myopel/main.sh 2
exit 0
