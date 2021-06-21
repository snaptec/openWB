#!/bin/bash


#Daten einlesen
xml=$(curl --max-time 10 -s http://$bezug_smartfox_ip/values.xml -XGET -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Host: $bezug_smartfox_ip'-H 'Connection: keep-alive')

#Aktuelle Leistung (kW --> W)
wattbezug=$(awk -F'[<>]' '/<value id="u5790-41">/{print $3}' <<< $xml)
wattbezug="${wattbezug::-2}"

wattbezug1=$(awk -F'[<>]' '/<value id="u6017-41">/{print $3}' <<< $xml)

wattbezug2=$(awk -F'[<>]' '/<value id="u6014-41">/{print $3}' <<< $xml)

wattbezug3=$(awk -F'[<>]' '/<value id="u6011-41">/{print $3}' <<< $xml)

#Zählerstand Import(kWh)
ikwh=$(awk -F'[<>]' '/<value id="u5827-41">/{print $3}' <<< $xml)
ikwh="${ikwh::-4}"
ikwh=$(echo "scale=2; $ikwh * 1000" | bc)

#Zählerstand Export(kWh)
ekwh=$(awk -F'[<>]' '/<value id="u5824-41">/{print $3}' <<< $xml)
ekwh="${ekwh::-4}"
ekwh=$(echo "scale=2; $ekwh * 1000" | bc)

#Weitere Zählerdaten für die Statusseite (PowerFaktor, Spannung und Strom)
evupf1=$(awk -F'[<>]' '/<value id="u6074-41">/{print $3}' <<< $xml)
evupf2=$(awk -F'[<>]' '/<value id="u6083-41">/{print $3}' <<< $xml)
evupf3=$(awk -F'[<>]' '/<value id="u6086-41">/{print $3}' <<< $xml)
evuv1=$(awk -F'[<>]' '/<value id="u5978-41">/{print $3}' <<< $xml)
evuv2=$(awk -F'[<>]' '/<value id="u5981-41">/{print $3}' <<< $xml)
evuv3=$(awk -F'[<>]' '/<value id="u5984-41">/{print $3}' <<< $xml)
bezuga1=$(awk -F'[<>]' '/<value id="u5999-41">/{print $3}' <<< $xml)
bezuga2=$(awk -F'[<>]' '/<value id="u5996-41">/{print $3}' <<< $xml)
bezuga3=$(awk -F'[<>]' '/<value id="u5993-41">/{print $3}' <<< $xml)
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
