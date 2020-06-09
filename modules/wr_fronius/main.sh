#!/bin/bash

# Auslesen eine Fronius Symo WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wirkleistung in [W].

pvwatttmp=$(curl --connect-timeout 3 -s "$wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope=System")
pvwatt=$(echo $pvwatttmp | jq '.Body.Data.Site.P_PV' | sed 's/\..*$//')

# Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
re='^-?[0-9]+$'
if ! [[ $pvwatt =~ $re ]] ; then
   pvwatt="0"
fi

pvkwh=$(echo $pvwatttmp | jq '.Body.Data.Site.E_Total' | sed 's/\..*$//')

if [[ $wrfronius2ip != "none" ]]; then
	pv2watttmp=$(curl --connect-timeout 3 -s "$wrfronius2ip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope=System")
	pv2watt=$(echo $pv2watttmp | jq '.Body.Data.Site.P_PV' | sed 's/\..*$//')
	# Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0
	re='^-?[0-9]+$'
	if ! [[ $pv2watt =~ $re ]] ; then
	   pv2watt="0"
	fi
	pvwatt=$(echo "($pvwatt + $pv2watt) * -1" | bc)
	echo $pvwatt
	# Zur weiteren Verwendung im Webinterface
	echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
	pv2kwh=$(echo $pv2watttmp | jq '.Body.Data.Site.E_Total')
	pvgkwh=$(echo "$pvkwh + $pv2kwh" | bc)
	if [[ $pvgkwh =~ $re ]] ; then
		if (( pvgkwh > 0 )); then
			echo $pvgkwh > /var/www/html/openWB/ramdisk/pvkwh
			pvkwhk=$(echo "scale=3; $pvgkwh / 1000" | bc)
			echo $pvkwhk > /var/www/html/openWB/ramdisk/pvkwhk
		fi
	fi
else
	pvwatt=$(echo "$pvwatt * -1" | bc)
	echo $pvwatt
	# Zur weiteren Verwendung im Webinterface
	echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
	if [[ $pvkwh =~ $re ]] ; then
		if (( pvkwh > 0 )); then
			echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
			pvkwhk=$(echo "scale=3; $pvkwh / 1000" | bc)
			echo $pvkwhk > /var/www/html/openWB/ramdisk/pvkwhk
		fi
	fi
fi
