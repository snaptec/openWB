#!/bin/bash

# Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
# Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv).
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen
# Achtung! Das Smart Meter muss im Einspeisepunkt sitzen, nicht im Verbrauchszweig!

. /var/www/html/openWB/openwb.conf

response=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=0")

wattbezug=$(echo "scale=0; $(echo $response | jq '.Body.Data.PowerReal_P_Sum')/1" | bc)
evuv1=$(echo "scale=2; $(echo $response | jq '.Body.Data.Voltage_AC_Phase_1')/1" | bc)
evuv2=$(echo "scale=2; $(echo $response | jq '.Body.Data.Voltage_AC_Phase_2')/1" | bc)
evuv3=$(echo "scale=2; $(echo $response | jq '.Body.Data.Voltage_AC_Phase_3')/1" | bc)
bezugw1=$(echo "scale=2; $(echo $response | jq '.Body.Data.PowerReal_P_Phase_1')/1" | bc)
bezugw2=$(echo "scale=2; $(echo $response | jq '.Body.Data.PowerReal_P_Phase_2')/1" | bc)
bezugw3=$(echo "scale=2; $(echo $response | jq '.Body.Data.PowerReal_P_Phase_3')/1" | bc)
evupf1=$(echo "scale=2; $(echo $response | jq '.Body.Data.PowerFactor_Phase_1')/1" | bc)
evupf2=$(echo "scale=2; $(echo $response | jq '.Body.Data.PowerFactor_Phase_2')/1" | bc)
evupf3=$(echo "scale=2; $(echo $response | jq '.Body.Data.PowerFactor_Phase_3')/1" | bc)
ikwh=$(echo $response | jq '.Body.Data.EnergyReal_WAC_Sum_Consumed')
ekwh=$(echo $response | jq '.Body.Data.EnergyReal_WAC_Sum_Produced')

# TODO: Diese direkte Rückgabe ist aktuell nötig.
#       Warum wird der Wert nicht wie alle anderen auch aus der Ramdisk geholt?
echo $wattbezug
# Schreiben alle Werte in die Ramdisk.
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $evuv1 > /var/www/html/openWB/ramdisk/evuv1
echo $evuv2 > /var/www/html/openWB/ramdisk/evuv2
echo $evuv3 > /var/www/html/openWB/ramdisk/evuv3
echo $bezugw1 > /var/www/html/openWB/ramdisk/bezugw1
echo $bezugw2 > /var/www/html/openWB/ramdisk/bezugw2
echo $bezugw3 > /var/www/html/openWB/ramdisk/bezugw3
# Berechne den Strom und lese ihn nicht direkt (der eigentlich zu lesende direkte Wert
# "Current_AC_Phase_1" wäre der Absolutwert und man würde das Vorzeichen verlieren)
bezuga1=$(echo "scale=2; $bezugw1 / $evuv1" | bc)
bezuga2=$(echo "scale=2; $bezugw2 / $evuv2" | bc)
bezuga3=$(echo "scale=2; $bezugw3 / $evuv3" | bc)
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3
echo $evupf1 > /var/www/html/openWB/ramdisk/evupf1
echo $evupf2 > /var/www/html/openWB/ramdisk/evupf2
echo $evupf3 > /var/www/html/openWB/ramdisk/evupf3
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
