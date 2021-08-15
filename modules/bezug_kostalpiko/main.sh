#!/bin/bash

#Auslesen eines Kostal Piko WR über die integrierte API des WR mit angeschlossenem Eigenverbrauchssensor.

pvwatttmp=$(curl --connect-timeout 3 -s $wrkostalpikoip/api/dxs.json?dxsEntries=33556736'&'dxsEntries=251658753'&'dxsEntries=83887106'&'dxsEntries=83887362'&'dxsEntries=83887618)

#aktuelle Ausgangsleistung am WR [W]
pvwatt=$(echo $pvwatttmp | jq '.dxsEntries[0].value' | sed 's/\..*$//')

if [ $pvwatt > 5 ] ; then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi

#zur weiteren verwendung im webinterface
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
#Gesamtzählerstand am WR [kWh]
pvkwh=$(echo $pvwatttmp | jq '.dxsEntries[1].value' | sed 's/\..*$//')
pvkwh=$(echo "$pvkwh*1000" |bc)
#zur weiteren verwendung im webinterface
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh

bezugw1=$(echo $pvwatttmp | jq '.dxsEntries[2].value' | sed 's/\..*$//')
bezugw2=$(echo $pvwatttmp | jq '.dxsEntries[3].value' | sed 's/\..*$//')
bezugw3=$(echo $pvwatttmp | jq '.dxsEntries[4].value' | sed 's/\..*$//')
if [[ "$speichermodul" == "speicher_bydhv" ]]; then
	speicherleistung=$(</var/www/html/openWB/ramdisk/speicherleistung)
	wattbezug=$(echo "$bezugw1+$bezugw2+$bezugw3+$pvwatt+$speicherleistung" | bc) 
else
	wattbezug=$(echo "$bezugw1+$bezugw2+$bezugw3+$pvwatt" |bc)
fi

echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
bezuga1=$(echo "scale=2 ; $bezugw1 / 225" | bc)
bezuga2=$(echo "scale=2 ; $bezugw2 / 225" | bc)
bezuga3=$(echo "scale=2 ; $bezugw3 / 225" | bc)
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3
