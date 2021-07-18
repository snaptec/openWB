#!/bin/bash

# Auslesen eines Kostal Piko WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung.
if [[ "$speichermodul" != "none" ]]; then
	pvwatttmp=$(curl --connect-timeout 5 -s $pv2ip/api/dxs.json?dxsEntries=33556736'&'dxsEntries=251658753)
else
	pvwatttmp=$(curl --connect-timeout 5 -s $pv2ip/api/dxs.json?dxsEntries=67109120'&'dxsEntries=251658753)
fi

# aktuelle Ausgangsleistung am WR [W]
pvwatt=$(echo $pvwatttmp | jq '.dxsEntries[0].value' | sed 's/\..*$//')

if [ $pvwatt > 5 ]
	then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi

echo $pvwatt
# zur weiteren verwendung im webinterface
echo $pvwatt > /var/www/html/openWB/ramdisk/pv2watt
# Gesamtzählerstand am WR [kWh]
# pvkwh=$(echo $pvwatttmp | jq '.dxsEntries[1].value' | sed 's/\..*$//')
# echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwhk
# pvkwh=$(echo "$pvkwh*1000" |bc)
# zur weiteren verwendung im webinterface
# echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
