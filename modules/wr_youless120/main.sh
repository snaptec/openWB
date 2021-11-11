#!/bin/bash

# Auslesen vom S0-Eingang eines Youless LS120 Energy Monitor.
answer=$(curl --connect-timeout 5 -s $wryoulessip/a?f=j)
if [[ $wryoulessalt == 0 ]]; then
	# aktuelle Ausgangsleistung am WR [W]
	pvwatt=$(echo $answer | jq -r '.ps0' | sed 's/\..*$//')
	# Gesamtz‰hlerstand am WR [Wh]
	pvkwh=$(echo $answer | jq -r '.cs0' | sed 's/,//g')
else
	# aktuelle Ausgangsleistung am WR [W]
	pvwatt=$(echo $answer | jq -r '.pwr' | sed 's/\..*$//')
	# Gesamtz‰hlerstand am WR [Wh]
	pvkwh=$(echo $answer | jq -r '.cnt' | sed 's/,//g')
fi

if (( $pvwatt > 5 )); then
	pvwatt=$(echo "$pvwatt*-1" |bc)
fi
echo $pvwatt
echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh
# Gesamtzählerstand am WR [kWh]
pvkwh=$(echo "$pvkwh/1000" |bc)
echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwhk
