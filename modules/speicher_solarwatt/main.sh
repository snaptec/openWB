#!/bin/bash

DMOD="MAIN"
Debug=$debug

openwbDebugLog ${DMOD} 1 "URL: ${speicher1_ip}/rest/kiwigrid/wizard/devices"
sresponse=$(curl --connect-timeout 5 -s "http://${speicher1_ip}/rest/kiwigrid/wizard/devices")
#sresponse=$(curl --connect-timeout 5 -s "http://192.168.178.64/rest/kiwigrid/wizard/devices")
openwbDebugLog ${DMOD} 1 "Resp: $?"
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

speichere=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerConsumedFromStorage.value != null) | .tagValues.PowerConsumedFromStorage.value' | sed 's/\..*$//') 
openwbDebugLog ${DMOD} 1 "Speichere: ${speichere}"
speicherein=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerOutFromStorage.value != null) | .tagValues.PowerOutFromStorage.value' | sed 's/\..*$//') 
openwbDebugLog ${DMOD} 1 "Speicherein: ${speicherein}"
speicheri=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.PowerBuffered.value != null) | .tagValues.PowerBuffered.value' | sed 's/\..*$//') 
openwbDebugLog ${DMOD} 1 "Speicheri: ${speicheri}"
#speicherleistung=$((speichere + speicherin - speicheri)) 
speicherleistung=$(echo "scale=0; ($speichere + $speicherin - $speicheri) *-1" | bc) 
openwbDebugLog ${DMOD} 1 "Speicherleistung: ${speicherleistung}"
echo $speicherleistung > /var/www/html/openWB/ramdisk/speicherleistung 
#echo "Batterieladung/entladung $speicherleistung" 
speichersoc=$(echo $sresponse | jq '.result.items | .[] | select(.tagValues.StateOfCharge.value != null) | .tagValues.StateOfCharge.value' | sed 's/\..*$//') 
openwbDebugLog ${DMOD} 1 "SpeicherSoC: ${speichersoc}"
#echo "Batterieladezustand $speichersoc" 
echo $speichersoc > /var/www/html/openWB/ramdisk/speichersoc 
