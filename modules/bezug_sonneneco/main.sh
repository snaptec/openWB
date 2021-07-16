#!/bin/bash

#Auslesen einer Sonnbenbatterie Eco 4.5 über die integrierte JSON-API des Batteriesystems
ra='^-?[0-9]+$'
if (( sonnenecoalternativ == 2 )); then
	evubezug=$(curl --connect-timeout 5 -s "$sonnenecoip:7979/rest/devices/battery/M39")
	evueinspeisung=$(curl --connect-timeout 5 -s "$sonnenecoip:7979/rest/devices/battery/M38")
	evubezug=$(echo $evubezug | sed 's/\..*$//')
	evueinspeisung=$(echo $evueinspeisung | sed 's/\..*$//')
	wattbezug=$(echo "$evubezug - $evueinspeisung" | bc)

	echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
	echo $wattbezug
else
	if (( sonnenecoalternativ == 1 )); then
		speicherantwort=$(curl --connect-timeout 5 -s "$sonnenecoip/api/v1/status")
		wattbezug=$(echo $speicherantwort | jq .GridFeedIn_W)
		# Negativ ist Verbrauch, positiv Einspeisung
		wattbezug=$(echo "$wattbezug * -1" | bc)
		# Es wird nur eine Spannung ausgegeben
		evuv1=$(echo $speicherantwort | jq .Uac)
		evuv2=$evuv1
		evuv3=$evuv1
		evuhz=$(echo $speicherantwort | jq .Fac)
		# Weitere Daten müssen errechnet werden
		# Es wird angenommen, dass alle Phasen gleich ausgelastet sind
		bezugw1=$(echo "$wattbezug / 3" | bc -l | awk '{printf "%.2f", $0}')
		bezugw2=$bezugw1
		bezugw3=$bezugw1
		bezuga1=$(echo "$bezugw1 / $evuv1" | bc -l | awk '{printf "%.2f", $0}')
		bezuga2=$bezuga1
		bezuga3=$bezuga1
		# Weitere Daten können nicht ermittelt werden
		evupf1=1
		evupf2=1
		evupf3=1
		ikwh=0
		ekwh=0
	else
		# Bietet die Rest API die Daten?
		exit 0
	fi
	# Gib den wichtigsten Wert direkt zurück (auch sinnvoll beim Debuggen).
	# echo $speicherantwort
	echo $wattbezug
	# echo $evuv1
	# echo $evuv2
	# echo $evuv3
	# echo $bezugw1
	# echo $bezugw2
	# echo $bezugw3
	# echo $bezuga1
	# echo $bezuga2
	# echo $bezuga3
	# echo $evuhz
	# echo $evupf1
	# echo $evupf2
	# echo $evupf3
	# echo $ikwh
	# echo $ekwh

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
fi
