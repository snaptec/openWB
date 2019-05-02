#!/bin/bash

#Auslesen eine Fronius Symo WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung
. /var/www/html/openWB/openwb.conf

#pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
#pvwatt=$(echo $pvwatttmp | jq '.Body.Data.PAC.Values' | sed 's/.*://' | tr -d '\n' | sed 's/^.\{2\}//' | sed 's/.$//' )
pvwatttmp=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope?System")
pvwatt=$(echo $pvwatttmp | jq '.Body.Data.Site.P_PV' |sed 's/\..*$//')
pvwatt=$(echo "$pvwatt * -1" | bc)

#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
re='^-?[0-9]+$'
if ! [[ $pvwatt =~ $re ]] ; then
   pvwatt="0"
fi
echo $pvwatt
#zur weiteren verwendung im webinterface
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt


pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)

pvkwh=$(echo $pvwatttmp | jq '.Body.Data.TOTAL_ENERGY.Values' | sed '2!d' |sed 's/.*: //' )
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
