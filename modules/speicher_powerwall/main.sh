#!/bin/bash
OPENWBBASEDIR=$(cd `dirname $0`/../../ && pwd)
RAMDISKDIR="$OPENWBBASEDIR/ramdisk"
MODULEDIR=$(cd `dirname $0` && pwd)

cookieOptions=""

if (( speicherpwloginneeded == 1 )); then
	# log in and save cookie for later use
	curl -s -k -i -c $MODULEDIR/cookie.txt -X POST -H "Content-Type: application/json" -d "{\"username\":\"customer\",\"password\":\"$speicherpwpass\", \"email\":\"$speicherpwuser\",\"force_sm_off\":false}" "https://$speicherpwip/api/login/Basic"
	# tell next curl calls to use saved cookie
	cookieOptions="-b $MODULEDIR/cookie.txt -c $MODULEDIR/cookie.txt"
fi

# read current load
speicherwatttmp=$(curl -k $cookieOptions --connect-timeout 5 -s "https://$speicherpwip/api/meters/aggregates")
speicherwatt=$(echo $speicherwatttmp | jq .battery.instant_power | sed 's/\..*$//')
speicherwatt=$(echo "$speicherwatt * -1" | bc)
ra='^[-+]?[0-9]+\.?[0-9]*$'
if ! [[ $speicherwatt =~ $ra ]] ; then
	speicherwatt="0"
fi
echo $speicherwatt > /var/www/html/openWB/ramdisk/speicherleistung

# read current SoC
speichersoc=$(curl -k $cookieOptions --connect-timeout 5 -s "https://$speicherpwip/api/system_status/soe")
soc=$(echo $speichersoc | jq .percentage)
soc=$(echo "($soc+0.5)/1" | bc)
if ! [[ $soc =~ $ra ]] ; then
	soc="0"
fi
echo $soc > /var/www/html/openWB/ramdisk/speichersoc
