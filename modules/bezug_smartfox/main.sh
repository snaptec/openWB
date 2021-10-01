#!/bin/bash

#Anpassung der Variablennamen nach Firmwareupgrade auf EM2 00.01.03.06 (04-2021)
#Daten einlesen
xml=$(curl --max-time 10 -s http://$bezug_smartfox_ip/values.xml -XGET -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Host: $bezug_smartfox_ip'-H 'Connection: keep-alive')

#Version ermitteln
version=$(awk -F'[<>]' '/<value id="version">/{print $3}' <<< $xml)
if ! [[ ${#version} > 6 ]] ; then
	versionshort="${version::-6}"
else
	versionshort="oldversion"
fi

if ! [[ "$versionshort" == "EM2 00.01" ]] ; then
	newversion=$true
	var_wattbezug="detailsPowerValue"
	var_wattbezug1="powerL1Value"
	var_wattbezug2="powerL2Value"
	var_wattbezug3="powerL3Value"
	var_ikwh="energyValue"
	var_ekwh="eToGridValue"
	var_evupf1="not_available"
	var_evupf2="not_available"
	var_evupf3="not_available"
	var_evuv1="voltageL1Value"
	var_evuv2="voltageL2Value"
	var_evuv3="voltageL3Value"
	var_bezuga1="ampereL1Value"
	var_bezuga2="ampereL2Value"
	var_bezuga3="ampereL3Value"
else
	newversion=$false
	var_wattbezug="u5790-41"
	var_wattbezug1="u6017-41"
	var_wattbezug2="u6014-41"
	var_wattbezug3="u6011-41"
	var_ikwh="u5827-41"
	var_ekwh="u5824-41"
	var_evupf1="u6074-41"
	var_evupf2="u6083-41"
	var_evupf3="u6086-41"
	var_evuv1="u5978-41"
	var_evuv2="u5981-41"
	var_evuv3="u5984-41"
	var_bezuga1="u5999-41"
	var_bezuga2="u5996-41"
	var_bezuga3="u5993-41"
fi

#Aktuelle Leistung (kW --> W)
wattbezug=$(awk -F'[<>]' '/<value id="'"$var_wattbezug"'">/{print $3}' <<< $xml)
wattbezug="${wattbezug::-2}"
wattbezug1=$(awk -F'[<>]' '/<value id="'"$var_wattbezug1"'">/{print $3}' <<< $xml)
wattbezug2=$(awk -F'[<>]' '/<value id="'"$var_wattbezug2"'">/{print $3}' <<< $xml)
wattbezug3=$(awk -F'[<>]' '/<value id="'"$var_wattbezug3"'">/{print $3}' <<< $xml)

#Zählerstand Import(kWh)
ikwh=$(awk -F'[<>]' '/<value id="'"$var_ikwh"'">/{print $3}' <<< $xml)
ikwh="${ikwh::-4}"
ikwh=$(echo "scale=2; $ikwh * 1000" | bc)

#Zählerstand Export(kWh)
ekwh=$(awk -F'[<>]' '/<value id="'"$var_ekwh"'">/{print $3}' <<< $xml)
ekwh="${ekwh::-4}"
ekwh=$(echo "scale=2; $ekwh * 1000" | bc)

#Weitere Zählerdaten für die Statusseite (PowerFaktor, Spannung und Strom)
#Powerfaktor ist nach dem Firmwareupgrade auf EM2 00.01.03.06 (04-2021) nicht mehr in der values.xml daher fix auf 1
if ! [[ $newversion ]] ; then 
	evupf1=1
	evupf2=1
	evupf3=1
else
	evupf1=$(awk -F'[<>]' '/<value id="'"$var_evupf1"'">/{print $3}' <<< $xml)
	evupf2=$(awk -F'[<>]' '/<value id="'"$var_evupf3"'">/{print $3}' <<< $xml)
	evupf3=$(awk -F'[<>]' '/<value id="'"$var_evupf3"'">/{print $3}' <<< $xml)
fi
evuv1=$(awk -F'[<>]' '/<value id="'"$var_evuv1"'">/{print $3}' <<< $xml)
evuv2=$(awk -F'[<>]' '/<value id="'"$var_evuv2"'">/{print $3}' <<< $xml)
evuv3=$(awk -F'[<>]' '/<value id="'"$var_evuv3"'">/{print $3}' <<< $xml)
bezuga1=$(awk -F'[<>]' '/<value id="'"$var_bezuga1"'">/{print $3}' <<< $xml)
bezuga2=$(awk -F'[<>]' '/<value id="'"$var_bezuga2"'">/{print $3}' <<< $xml)
bezuga3=$(awk -F'[<>]' '/<value id="'"$var_bezuga3"'">/{print $3}' <<< $xml)
#Prüfen ob Werte gültig
re='^[-+]?[0-9]+\.?[0-9]*$'
if ! [[ $wattbezug =~ $re ]] ; then
	wattbezug=$(</var/www/html/openWB/ramdisk/wattbezug)
fi
if ! [[ $ikwh =~ $re ]] ; then
	ikwh=$(</var/www/html/openWB/ramdisk/bezugkwh)
fi
if ! [[ $ekwh =~ $re ]] ; then
	ekwh=$(</var/www/html/openWB/ramdisk/einspeisungkwh)
fi

#Ausgabe
echo $wattbezug
echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
echo $wattbezug1 > /var/www/html/openWB/ramdisk/bezugw1
echo $wattbezug2 > /var/www/html/openWB/ramdisk/bezugw2
echo $wattbezug3 > /var/www/html/openWB/ramdisk/bezugw3
echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
echo $evupf1 > /var/www/html/openWB/ramdisk/evupf1
echo $evupf2 > /var/www/html/openWB/ramdisk/evupf2
echo $evupf3 > /var/www/html/openWB/ramdisk/evupf3
echo $evuv1 > /var/www/html/openWB/ramdisk/evuv1
echo $evuv2 > /var/www/html/openWB/ramdisk/evuv2
echo $evuv3 > /var/www/html/openWB/ramdisk/evuv3
echo $bezuga1 > /var/www/html/openWB/ramdisk/bezuga1
echo $bezuga2 > /var/www/html/openWB/ramdisk/bezuga2
echo $bezuga3 > /var/www/html/openWB/ramdisk/bezuga3
