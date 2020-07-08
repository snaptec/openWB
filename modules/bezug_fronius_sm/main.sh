#!/bin/bash

# Auslesen eines Fronius Symo WR mit Fronius Smartmeter über die integrierte JSON-API des WR.
# Rückgabewert ist die aktuelle Einspeiseleistung (negativ) oder Bezugsleistung (positiv).
# Einspeiseleistung: PV-Leistung > Verbrauch, es wird Strom eingespeist
# Bezugsleistug: PV-Leistung < Verbrauch, es wird Strom aus dem Netz bezogen


# Fordere die Werte vom SmartMeter an.
response_sm=$(curl --connect-timeout 5 -s "$wrfroniusip/solar_api/v1/GetMeterRealtimeData.cgi?Scope=Device&DeviceID=1")

# Überprüfe den Einbauort des SmartMeters.
meter_location=$(echo $response_sm | jq '.Body.Data.Meter_Location_Current')
# Wenn das SmartMeter nicht im Verbrauchszweig (also im Einspeisepunkt) sitzt, verwende direkt dessen Werte.
if [[ $meter_location != "1" ]]; then
    # Lese alle wichtigen Werte aus der JSON-Antwort und skaliere sie gleich.
    wattbezug=$(echo "scale=0; $(echo $response_sm | jq '.Body.Data.PowerReal_P_Sum')/1" | bc)
    evuv1=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Voltage_AC_Phase_1')/1" | bc)
    evuv2=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Voltage_AC_Phase_2')/1" | bc)
    evuv3=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Voltage_AC_Phase_3')/1" | bc)
    bezugw1=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerReal_P_Phase_1')/1" | bc)
    bezugw2=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerReal_P_Phase_2')/1" | bc)
    bezugw3=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerReal_P_Phase_3')/1" | bc)
    # Berechne den Strom und lese ihn nicht direkt (der eigentlich zu lesende direkte Wert
    # "Current_AC_Phase_1" wäre der Absolutwert und man würde das Vorzeichen verlieren).
    bezuga1=$(echo "scale=2; $bezugw1 / $evuv1" | bc)
    bezuga2=$(echo "scale=2; $bezugw2 / $evuv2" | bc)
    bezuga3=$(echo "scale=2; $bezugw3 / $evuv3" | bc)
    evuhz=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Frequency_Phase_Average')/1" | bc)
    evupf1=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerFactor_Phase_1')/1" | bc)
    evupf2=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerFactor_Phase_2')/1" | bc)
    evupf3=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerFactor_Phase_3')/1" | bc)
    ikwh=$(echo $response_sm | jq '.Body.Data.EnergyReal_WAC_Sum_Consumed')
    ekwh=$(echo $response_sm | jq '.Body.Data.EnergyReal_WAC_Sum_Produced')
# ... ansonsten, wenn das SmartMeter im Verbrauchszweig sitzt, kombiniere dessen Werte mit denen des Wechselrichters.
else
    # Lese die aktuelle PV-Leistung des Wechselrichters ein.
    response_fi=$(curl --connect-timeout 3 -s "$wrfroniusip/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope=System")
    pvwatt=$(echo $response_fi | jq '.Body.Data.Site.P_PV' | sed 's/\..*$//')
    # Wenn WR aus bzw. im Standby (keine Antwort), ersetze leeren Wert durch eine 0.
    re='^-?[0-9]+$'
    if ! [[ $pvwatt =~ $re ]] ; then
        pvwatt="0"
    fi
    
    wattbezug=$(echo "scale=0; $(echo $response_fi | jq '.Body.Data.Site.P_Grid')/1" | bc)
    # Hier gehen wir mal davon aus, dass es keinen großen Unterschied zwischen Verbrauchs- und Einspeisepunkt gibt.
    evuv1=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Voltage_AC_Phase_1')/1" | bc)
    evuv2=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Voltage_AC_Phase_2')/1" | bc)
    evuv3=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Voltage_AC_Phase_3')/1" | bc)
    # Hier gehen wir mal davon aus, dass der Wechselrichter seine PV-Leistung gleichmäßig auf alle Phasen aufteilt.
    bezugw1=$(echo "scale=2; (-1 * $(echo $response_sm | jq '.Body.Data.PowerReal_P_Phase_1') - $pvwatt/3)/1" | bc)
    bezugw2=$(echo "scale=2; (-1 * $(echo $response_sm | jq '.Body.Data.PowerReal_P_Phase_2') - $pvwatt/3)/1" | bc)
    bezugw3=$(echo "scale=2; (-1 * $(echo $response_sm | jq '.Body.Data.PowerReal_P_Phase_3') - $pvwatt/3)/1" | bc)
    # Berechne den Strom und lese ihn nicht direkt (der eigentlich zu lesende direkte Wert
    # "Current_AC_Phase_1" wäre der Absolutwert und man würde das Vorzeichen verlieren).
    bezuga1=$(echo "scale=2; $bezugw1 / $evuv1" | bc)
    bezuga2=$(echo "scale=2; $bezugw2 / $evuv2" | bc)
    bezuga3=$(echo "scale=2; $bezugw3 / $evuv3" | bc)
    evuhz=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.Frequency_Phase_Average')/1" | bc)
    # Hier gehen wir mal davon aus, dass der Wechselrichter vor dem SmartMeter den Leistungsfaktor nicht
    # maßgeblich beeinflusst. Falls dies falsch ist -> Leistungsfaktor auf 0 setzen!
    evupf1=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerFactor_Phase_1')/1" | bc)
    evupf2=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerFactor_Phase_2')/1" | bc)
    evupf3=$(echo "scale=2; $(echo $response_sm | jq '.Body.Data.PowerFactor_Phase_3')/1" | bc)
    # Beim Energiebezug ist nicht klar, welcher Anteil aus dem Netz bezogen wurde, und was aus dem Wechselrichter kam.
    #ikwh=$(echo $response_sm | jq '.Body.Data.EnergyReal_WAC_Sum_Consumed')
    ikwh=0
    # Beim Energieexport ist nicht klar, wie hoch der Eigenverbrauch während der Produktion war.
    #ekwh=$(echo $response_fi | jq '.Body.Data.Site.E_Total')
    ekwh=0
fi

# Gib den wichtigsten Wert direkt zurück (auch sinnvoll beim Debuggen).
echo $wattbezug

# Schreibe alle Werte in die Ramdisk.
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $evuv1 > /var/www/html/openWB/ramdisk/evuv1
echo $evuv2 > /var/www/html/openWB/ramdisk/evuv2
echo $evuv3 > /var/www/html/openWB/ramdisk/evuv3
echo $bezugw1 > /var/www/html/openWB/ramdisk/bezugw1
echo $bezugw2 > /var/www/html/openWB/ramdisk/bezugw2
echo $bezugw3 > /var/www/html/openWB/ramdisk/bezugw3
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3
echo $evuhz > /var/www/html/openWB/ramdisk/evuhz
echo $evupf1 > /var/www/html/openWB/ramdisk/evupf1
echo $evupf2 > /var/www/html/openWB/ramdisk/evupf2
echo $evupf3 > /var/www/html/openWB/ramdisk/evupf3
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
