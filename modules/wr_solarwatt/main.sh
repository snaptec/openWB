#!/bin/bash

#!/bin/bash

sresponse=$(curl --connect-timeout 3 -s "http://$speichersolarwattip/rest/kiwigrid/wizard/devices")

#pvwh=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.WorkProduced.value != null) | .tagValues.WorkProduced.value' | sed 's/\..*$//')
#echo "PV erzeugt $pvwh"
#echo $pvwh > /var/www/html/openWB/ramdisk/pvkwh
pvwatt=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerProduced.value != null) | .tagValues.PowerProduced.value' | sed 's/\..*$//')
pvwatt=$((pvwatt * -1))
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvwatt
