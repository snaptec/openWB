# openWB




Die Software steht frei für jeden zur Verfügung, siehe GPLv3 Bedingungen.

	Unterstüztung ist gerne gesehen!
	Sei es in Form von Code oder durch Spenden
	Spenden bitte an spenden@openwb.de

Anfragen für Supportverträge an info@openwb.de
Weitere Infos unter https://openwb.de

# Haftungsausschluss
Es wird mit Kleinspannung aber auch 220V beim Anschluss der EVSE gearbeitet. 
Dies darf nur geschultes Personal. Die Anleitung ist ohne Gewähr und jegliches Handeln basiert auf eigene Gefahr.
Eine Fehlkonfiguration der Software kann höchstens ein nicht geladenes Auto bedeuten.
Falsch zusammengebaute Hardware kann lebensgefährlich sein. Im Zweifel diesen Part von einem Elektriker durchführen lassen.
Keine Gewährleistung für die Software - use at your own RISK!

# Wofür?
Steuerung einer EVSE DIN oder anderer Ladepunkte für sofortiges laden, Überwachung der Ladung, PV Überschussladung und Lastmanagement mehrerer WB.

Unterstützt wird jedes EV das den AC Ladestandard unterstützt.





# Bezug
openWB gibt es unter 

	https://openwb.de/shop/



# Installation


Bei fertigen openWB vorinstalliert



Software:

Installiertes Raspbian auf einem Raspberry pi 3.

Installationsanleitung für Windows: http://openwb.de/main/wp-content/uploads/2019/07/install_openWB_v2.pdf

Raspbian installieren

	https://www.raspberrypi.org/downloads/raspbian/

In der Shell folgendes eingeben:

	curl -s https://raw.githubusercontent.com/snaptec/openWB/master/openwb-install.sh | sudo sh



Crontab anpassen:
	crontab -e
hier einfügen:

	* * * * * /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 10 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 20 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 30 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 40 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 50 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 



 


# Extras

 Bei Nutzung von einem USR-TCP232-410 Lan to Modbus Converter folgende Konfiguration verwenden:

	Baud Rate: 9600
	Data Size: 8 Bit
	Parity: None
	Stop Bits: 1
	Flow COntrol and RS485: RS485
	Local Port Number: 26
	Remote Port Number: 26
	Worke Mode: TCP Server None
	TCP Server detail: default Type
	Timeout: 0
	UART packet Time: 10 ms
	UART packet length: 512 chars


Der Raspberry funktioniert zuverlässig mit gutem WLAN. Lan Kabel ist zu bevorzugen.

Taster am Raspberry zur Einstellung des Lademodi

Der Lademodi kann nicht nur über die Weboberfläche sondern auch an der Wallbox direkt eingestellt werden.
Hierzu müssen schließer Taster von GND (Pin 34) nach Gpio X  angeschlossen werden.

	SofortLaden GPIO 12, PIN 32

	Min+PV GPIO 16, PIN 36

	NurPV GPIO 6, Pin 31

	Aus Gpio 13, Pin 33
	




# Module erstellen

Ist ein Modul für den gewünscht Einsatszweck noch nicht verfügbar kann man dies selbst erstellen.
Wenn es läuft bitte reporten und es (einstellbar) dem Projekt hinzugefügt.

Ein Modul ist immer ein Ordner mit dem Modulnamen im Ordner openWB/modules. Es besteht aus einem Shell script mit dem Namen main.sh. Sollten weitere Dateien benötigt werden liegen diese mit im Ordner. 

Exemplarisch der Aufbau erklärt am bezug_http Modul:


	#!/bin/bash
	#Die eigentliche (in dem Fall http) Abfrage. Die Variable sollte den Modulnamen und im Anschluss den Wert enthalten um sie eindeutig zu identifizieren
	wattbezug=$(curl --connect-timeout 10 -s $bezug_http_w_url)
	#Prüfung auf Richtigkeit der Variable. Sie darf bei bezug modulen ein - enthalten sowie die Zahlen 0-9
	re='^-?[0-9]+$'
	# Entspricht der abgefragte Wert nicht der Anforderung wird sie auf 0 gesetzt um ein Fehlverhalten der Regelung zu verhindern
	if ! [[ $wattbezug =~ $re ]] ; then
		wattbezug="0"
	fi
	#Der Hauptwert (Watt) wird als echo an die Regellogik zurückgegeben
	echo $wattbezug
	#Zusätzlich wird der Wert in die Ramdisk geschrieben, dies ist für das Webinterface sowie das Logging und ggf. externe Abfragen
	echo $wattbezug > /var/www/html/openWB/ramdisk/wattbezug
	#Wird Logging von metern genutzt wird der absolute Zählerstand in Wh benötigt. Ist dieser nicht vorhanden sollte die Variable auf none gesetzt werden
	if [[ $bezug_http_ikwh_url != "none" ]]; then
		ikwh=$(curl --connect-timeout 5 -s $bezug_http_ikwh_url)
		echo $ikwh > /var/www/html/openWB/ramdisk/bezugkwh
	fi
	#Analog zum bezug dasselbe Verfahren für die Einspeisung
	if [[ $bezug_http_ekwh_url != "none" ]]; then
		ekwh=$(curl --connect-timeout 5 -s $bezug_http_ekwh_url)
		echo $ekwh > /var/www/html/openWB/ramdisk/einspeisungkwh
	fi


Bei PV Modulen muss geschrieben werden:

	#Rückgabewert in Watt
	echo $pvwatt
	echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
	#ggf wenn verfügbar für logging den Zählerstand in Wh
	echo $pvwh > /var/www/html/openWB/ramdisk/pvkwh

Beispielhaft das wr_fronius modul für deren Wechselrichter mit Webinterface:
Fronius bietet eine Json API an. Diese wird hier auf die Werte die gebraucht werden reduziert.


	#!/bin/bash
	#Auslesen eine Fronius Symo WR über die integrierte API des WR. Rückgabewert ist die aktuelle Wattleistung
	#Abfrage der kompletten Json Rückgabe
	pvwatttmp=$(curl --connect-timeout 5 -s $wrfroniusip/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System)
	# Das Tool jq verarbeitet die Rückgabe und reduziert sie auf die gewünschte Zeile. sed & tr entfernen ungewollte Klammern, Punkte und \n newline Zeichen um die reine Zahl zu erhalten
	pvwatt=$(echo $pvwatttmp | jq '.Body.Data.PAC.Values' | sed 's/.*://' | tr -d '\n' | sed 's/^.\{2\}//' | sed 's/.$//' )
	#wenn WR aus bzw. im standby (keine Antwort) ersetze leeren Wert durch eine 0
	#Fronius Wechselrichter gehen nachts in den Standby und antworten dann nicht. Um einen Fehler abzufangen bei leerer Rückgabe wird eine 0 gesetzt
	re='^[0-9]+$'
	if ! [[ $pvwatt =~ $re ]] ; then
	   pvwatt="0"
	fi
	#Rückgabe des Watt Wertes an die Regellogik
	echo $pvwatt
	#zur weiteren verwendung im webinterface, zum Logging & zur externen Abfrage
	echo $pvwatt > /var/www/html/openWB/ramdisk/pvwatt
	#Aus dem selben String erhält man ebenso den totalen Zählerstand für das Logging
	#Hier sieht man das statt .Body.Data.PAC der Wert .Body.Data:TOTAL_Energy "ausgeschnitten" wird
	pvkwh=$(echo $pvwatttmp | jq '.Body.Data.TOTAL_ENERGY.Values' | sed '2!d' |sed 's/.*: //' )
	#Dieser Wert wird nun in die ramdisk gespeichert
	echo $pvkwh > /var/www/html/openWB/ramdisk/pvkwh


