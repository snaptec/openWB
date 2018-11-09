#!/bin/bash

#Auslesen eines Kostal Piko WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung.
. /var/www/html/openWB/openwb.conf

pvwatttmp=$(curl --connect-timeout 5 -s $wrkostalpikoip/api/dxs.json?dxsEntries=67109120'&'dxsEntries=251658753)


re='^[0-9]+$'
if ! [[ $pvwatt =~ $re ]] ; then
	   pvwatt="0"
   fi
#aktuelle Ausgangsleistung am WR [W]
pvwatt=$(echo $pvwatttmp | jq '.dxsEntries[0].value' | awk '{printf "%.0f", $1}')
#zur weiteren verwendung im webinterface
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt

#Gesamtzählerstand am WR [kWh]
pvkwh=$(echo $pvwatttmp | jq '.dxsEntries[1].value' | awk '{printf "%.0f", $1}')
#zur weiteren verwendung im webinterface
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
