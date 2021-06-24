#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in keballlp1
$OPENWBBASEDIR/modules/keballlp1/main.sh 2

exit 0
