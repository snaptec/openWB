#!/bin/bash

#Auslesen eines Kostal Piko WR über die integrierte API des WR. Rückgabewerte sind die aktuelle Wattleistung und der Gesamtzählerstand am WR.

. /var/www/html/openWB/openwb.conf

pvwatttmp=$(curl --connect-timeout 5 -s $wrkostalpikoip/api/dxs.json?dxsEntries=67109120&dxsEntries=251658753)

#Aktuelle Wattleistung, gerundet
pvwatt=$(echo $pvwatttmp | jq '.dxsEntries[0] | .value | round')

#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
re='^[0-9]+$'
if ! [[ $pvwatt =~ $re ]] ; then
	   pvwatt="0"
   fi
   echo $pvwatt

   #zur weiteren Verwendung im webinterface
   echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt

   # Gesamtzählerstand am WR, gerundet
   pvkwh=$(echo $pvwatttmp | jq '.dxsEntries[1] | .value | round')

   #zur weiteren Verwendung im webinterface
   echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
