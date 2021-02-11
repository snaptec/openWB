#!/bin/bash

OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)

# for backward compatibility only
# functionality is in soc_http
$OPENWBBASEDIR/modules/soc_http/main.sh 2
exit 0
