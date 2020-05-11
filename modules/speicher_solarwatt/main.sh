#!/bin/bash

sresponse=$(curl --connect-timeout 3 -s"http://$speichersolarwattip/rest/kiwigrid/wizard/devices")
pvwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkProduced.value')
echo "PV erzeugt $pvwh"
pvwatt=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerProduced.value')
echo "PV Leistung aktuellt $pvwatt"
bezugwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkConsumedFromGrid.value')
echo "Vom Netz bezogen Gesamt $bezugwh"
bezugw=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerConsumedFromGrid.value')
einspeisungw=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerOut.value')
bezugwatt=$((bezugw - einspeisungw))
echo "Bezug/Einspeisung am Übergabepunkt $bezugwatt"
einspeisungwh=$(echo $sresponse | jq '.result.items | .[0].tagValues.WorkOut.value')
echo "Ins Netz eingespeist Gesamt $einspeisungwh"
speichere=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerConsumedFromStorage.value')
speicherein=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerOutFromStorage.value')
speicheri=$(echo $sresponse | jq '.result.items | .[0].tagValues.PowerBuffered.value')
speicherleistung=$((speichere + speicherin - speicheri))
echo "Batterieladung/entladung $speicherleistung"
speichersoc=$(echo $sresponse | jq '.result.items | .[5].tagValues.StateOfCharge.value')
echo "Batterieladezustand $speichersoc"



