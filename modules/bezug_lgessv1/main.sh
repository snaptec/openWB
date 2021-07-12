#!/bin/bash
#
## ess_url: IP/URL des LG ESS V1.0
#
## ess_pass: Passwort, um sich in den LG ESS V1.0 einzuloggen
#            Das Passwort ist standardmäßig die Registrierungsnr.
#            die sich auf dem PCS (dem Hybridwechselrichter und
#            Batteriemanagementsystem) befindet (Aufkleber!). Alter-
#            nativ findet man die Registrierungsnr. in der App unter
#            dem Menüpunkt "Systeminformationen"
#            Mit der Registrierungsnr. kann man sich dann in der 
#            Rolle "installer" einloggen. 
ess_url="https://$lgessv1ip"
ess_pass=$lgessv1pass
#
## Flag für unterschiedliche API-Versionen der Firmware
#
if [ "$ess_api_ver" == "10.2019" ]; then
	arr_pos="13"
else 
	arr_pos="1"
fi
#
## Prüfen, ob ein Sessionkey in der Ramdisk vorhanden ist. Wenn nicht,
#  z.b. wenn das System neu gestartet wurde, dann wird ein Dummykey an-
#  gelegt
if test -f "/var/www/html/openWB/ramdisk/ess_session_key"; then
	session_key=$(sed -n '1p' /var/www/html/openWB/ramdisk/ess_session_key)
else
	session_key=" "
fi
#
## JSON-Objekt vom PCS abholen. Es können folgende JSON-Objekte zurück gegeben werden:
#
#  1. Wenn der Sessionkey nicht korrekt bzw. wenn die Session abgelaufen ist, dann wird ein
#     JSON-Objekt mit einem Attribut "auth_key" zurück gegeben
#  2. Der Sessionkey ist gültig, dann erhält man ein JSON-Objekt mit den wichtigsten Attribute.
#     Beispiel JSON-Objekte liegen im Ordner lgessv1/JSON-Beispiele.txt
#
json=$(curl -s -k --connect-timeout 5 -d '{"auth_key":'$session_key'}' -H "Content-Type: application/json" -X POST $ess_url'/v1/user/essinfo/home')
authchk=$(echo $json | jq '.auth' | sed 's/.*://' | tr -d '\n' | sed 's/\"//' | sed 's/\"//')
#
## Pruefen, ob Sessionkey ungültig ist, wenn ja, Login und neuen Sessionkey empfangen
#
if [ "$authchk" == "auth_key failed" ] || [ "$authchk" == "auth timeout" ] || [ "$authchk" == "" ]; then
	json=$(curl -s -k --connect-timeout 5 -d '{"password":"'$ess_pass'"}' -H "Content-Type: application/json" -X PUT $ess_url/v1/login)
	session_key=$(echo $json | jq '.auth_key' | sed 's/.*://' | tr -d '\n' | sed 's/\"//' | sed 's/\"//')
	session_key='"'$session_key'"'
	outjson='{"auth_key":'$session_key'}'
	#
	## aktuelle Daten aus dem PCS auslesen
	#
	json=$(curl -s -k --connect-timeout 5 -d $outjson -H '"Content-Type: application/json"' -X POST $ess_url/v1/user/essinfo/home)
	#
	## Sessionkey in der Ramdisk abspeichern
	#
	echo $session_key > /var/www/html/openWB/ramdisk/ess_session_key
fi
#
## JSON-Objekt auswerten
#
grid_power=$(echo $json | jq '.statistics.grid_power' | sed 's/.*://' | tr -d '\n' | sed 's/\"//' | sed 's/\"//')
is_grid_selling_=$(echo $json | jq '.direction.is_grid_selling_' | sed 's/.*://' | tr -d '\n' | sed 's/\"//' | sed 's/\"//')
load_power=$(echo $json | jq '.statistics.load_power' | sed 's/.*://' | tr -d '\n' | sed 's/\"//' | sed 's/\"//')
if [ "$is_grid_selling_" = "1" ]; then
	#grid_power='-'$grid_power
	grid_power=$(echo "$grid_power*-1" |bc)
fi
#
## Daten für Langzeitlog holen
#
jahr=$(date +%Y)
monat=$(date +%m)
arr_pos=$monat
year_of_stat='"'year'"':'"'$jahr'"'
json=$(curl -s -k --connect-timeout 5 -d '{"auth_key":'$session_key', '$year_of_stat'}' -H "Content-Type: application/json" -X POST $ess_url'/v1/user/graph/load/year')
ikwh=$(echo $json | jq '.loginfo['$arr_pos'].total_purchase' | sed 's/.*://' | tr -d '\n' | sed 's/\"//' | sed 's/\"//' | sed 's/kwh//' | sed 's/\.//')
loadkwh=$(echo $json | jq '.loginfo['$arr_pos'].total_consumption' | sed 's/.*://' | tr -d '\n' | sed 's/\"//' | sed 's/\"//' | sed 's/kwh//' | sed 's/\.//')
#
## Daten in Ramdisk schreiben
#
#echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
echo $grid_power > /var/www/html/openWB/ramdisk/wattbezug
echo $grid_power
