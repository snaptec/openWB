#!/bin/bash

sresponse=$(curl --connect-timeout 3 -s "http://$speichersolarwattip/rest/kiwigrid/wizard/devices")
#pvwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkProduced.value')
#echo "PV erzeugt $pvwh"
#pvwatt=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerProduced.value')
#echo "PV Leistung aktuellt $pvwatt"
#bezugwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkConsumedFromGrid.value')
#echo "Vom Netz bezogen Gesamt $bezugwh"
#bezugw=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerConsumedFromGrid.value')
#einspeisungw=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerOut.value')
#bezugwatt=$(echo "scale=0; $bezugw - $einspeisungw /1" |bc)
#echo "Bezug/Einspeisung am Übergabepunkt $bezugwatt"
#einspeisungwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkOut.value')
#echo "Ins Netz eingespeist Gesamt $einspeisungwh" 
speichere=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerConsumedFromStorage.value' | sed 's/\..*$//') 
speicherein=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerOutFromStorage.value' | sed 's/\..*$//') 
speicheri=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerBuffered.value' | sed 's/\..*$//') 
#speicherleistung=$((speichere + speicherin - speicheri)) 
speicherleistung=$(echo "scale=0; ($speichere + $speicherin - $speicheri) *-1" | bc) 
echo $speicherleistung > /var/www/html/openWB/ramdisk/speicherleistung 
#echo "Batterieladung/entladung $speicherleistung" 
speichersoc=$(echo $sresponse | jq '.result.items | .[7].tagValues.StateOfCharge.value' | sed 's/\..*$//') 
#echo "Batterieladezustand $speichersoc" 
echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc 

