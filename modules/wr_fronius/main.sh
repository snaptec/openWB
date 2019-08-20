#!/bin/bash

#Auslesen eine Fronius Symo WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung
. /var/www/html/openWB/openwb.conf

#pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
#pvwatt=$(echo $pvwatttmp | jq '.Body.Data.PAC.Values' | sed 's/.*://' | tr -d '\n' | sed 's/^.\{2\}//' | sed 's/.$//' )
pvwatttmp=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope?System")
pvwatt=$(echo $pvwatttmp | jq '.Body.Data.Site.P_PV' |sed 's/\..*$//')

#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
re='^-?[0-9]+$'
if ! [[ $pvwatt =~ $re ]] ; then
   pvwatt="0"
fi


pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)

pvkwh=$(echo $pvwatttmp | jq '.Body.Data.TOTAL_ENERGY.Values' | sed '2!d' |sed 's/.*: //' )

if [[ wrfronius2ip != "none" ]]; then
	pv2watttmp=$(curl --connect-timeout 5 -s "$wrfronius2ip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope?System")
	pv2watt=$(echo $pv2watttmp | jq '.Body.Data.Site.P_PV' |sed 's/\..*$//')
	#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
	re='^-?[0-9]+$'
	if ! [[ $pv2watt =~ $re ]] ; then
	   pv2watt="0"
	fi
	pvwatt=$(echo "($pvwatt + $pv2watt) * -1" | bc)
	echo $pvwatt
	#zur weiteren verwendung im webinterface
	echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
	pv2watttmp=$(curl --connect-timeout 5 -s $wrfronius2ip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
	pv2kwh=$(echo $pvwatttmp | jq '.Body.Data.TOTAL_ENERGY.Values' | sed '2!d' |sed 's/.*: //' )
	pvgkwh=$(echo "$pvkwh + $pv2kwh" | bc)
	echo $pvgkwh > /var/www/html/openWB/ramdisk/pvkwh
else
	pvwatt=$(echo "$pvwatt * -1" | bc)
	echo $pvwatt
	#zur weiteren verwendung im webinterface
	echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
	echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
fi
