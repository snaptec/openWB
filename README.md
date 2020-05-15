# openWB




Die Software steht frei für jeden zur Verfügung, siehe GPLv3 Bedingungen.

	Unterstüztung ist gerne gesehen!
	Sei es in Form von Code oder durch Spenden
	Spenden bitte an info@snaptec.org

Anfragen für Supportverträge ebenso an info@snaptec.org
Weitere Infos unter https://openwb.de

# Haftungsausschluss
Es wird mit Kleinspannung aber auch 220V beim Anschluss der EVSE gearbeitet. 
Dies darf nur geschultes Personal. Die Anleitung ist ohne Gewähr und jegliches Handeln basiert auf eigene Gefahr.
Eine Fehlkonfiguration der Software kann höchstens ein nicht geladenes Auto bedeuten.
Falsch zusammengebaute Hardware kann lebensgefährlich sein. Im Zweifel diesen Part von einem Elektriker durchführen lassen.
Keine Gewährleistung für die Software - use at your own RISK!

# Wofür?
Steuerung einer EVSE DIN oder anderer Ladepunkte für sofortiges laden, überwachung der Ladung, PV Überschussladung und Lastmanagement mehrerer WB.

Unterstützt wird jedes EV das den AC Ladestandard mit Typ 1 oder Typ 2 Stecker unterstützt.


# Was wird benötigt?
Hardware:


- EVSE DIN
- Raspberry Pi 3 + Gehäuse (ev. gleich Hutschienengehäuse zur Installation in der WB)
- USB RS 485 Adapter
- Stromzähler mit Modbus zur Ladeleistungsmessung (z.B. MPM3PM
- Bezugsstromzähler für +Bezug (positiv) bzw. -Überschuss (z.B. vorh. Smartmeter mit IR Lesekopf und VZLogger, separater Modbuszähler oder bereits vorhandene Lösung mit API, openWB EVU Kit)
- Auslesen der PV-Leistung (entsprechendes Softwaremodul fuer den Wechselrichter (z.B. Fronius) oder separater Zähler)
- Schuetz entsprechend der max. Leistung
- Ladekabel mit CP-Steuerleitung (CP => Control Pilot)
- Typ1/2 Stecker
- Ggf. ein FI Typ B



# Bausatz
OpenWB gibt es unter 

	https://openwb.de/shop/

auch als Bausatz fertig vorkonfiguriert inkl Anleitung zu kaufen.

Bausatz Anleitung:
	
	https://openwb.de/main/?page_id=135



# Installation


Siehe Verdrahtungsplan für die Hardware Verkabelung



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



Zum Updaten im Webinterface unter Misc den Update Button drücken.
 


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
	

# Danke geht an:

	Frank für das Bereitstellen von Hardware und sein Modbus Wissen!

# API für Remotesteuerung, Einbindung in Hausautomation,  etc..

Die openWB lässt sich per GET Requests fernsteuern. Derzeit implementiert:
- Lademodus
- Sofort Laden Stromstärke

Beispiel:

	curl -X GET 'http://ipdesraspi/openWB/web/api.php?jetztll=16'
stellt die Ladeleistung auf 16A

	curl -X GET 'http://ipdesraspi/openWB/web/api.php?lademodus=jetzt'
stellt den Lademodus auf Sofort Laden.

Gültige Werte:

jetztll

	10-32

lademodus

	jetzt
	minundpv
	pvuberschuss
	stop


Die API kann auch abgefragt werden und antwortet im Json Format
Nachfolgend die Werte zur Erklärung durch deren Einheit ersetzt

	curl -X GET 'http://ipdesraspi/openWB/web/api.php?get=all'
	{
	  "date": "2019:02:19-18:10:44", # aktuelles datum
	  "lademodus": "2", # lademodus (0 Sofort, 1 Min+PV, 2 NurPV, 3 Standby, 4 Stop)
	  "minimalstromstaerke": "6", # konfigurierte Minimalstromstärke
	  "maximalstromstaerke": "32", # konfigurierte Maximalstromstärke
	  "llsoll": "0", # Soll Ladestromvorgabe
	  "restzeitlp1": "5 Min", 
	  "restzeitlp2": "1 H 30 Min",
	  "restzeitlp3": "--",
	  "gelkwhlp1": "0", # im aktuellen Ladevorgang
	  "gelkwhlp2": "0", # im aktuellen Ladevorgang
	  "gelkwhlp3": "0", # im aktuellen Ladevorgang
	  "gelrlp1": "3", # im aktuellen Ladevorgang geladene km
	  "gelrlp2": "50", # im aktuellen Ladevorgang geladene km
	  "gelrlp3": "0", # im aktuellen Ladevorgang geladene km
	  "llgesamt": "0", # Ladeleistung aller Ladepunkte summiert
	  "evua1": "2.5657", # Ampere Bezug am EVU
	  "evua2": "2.6333", # Ampere Bezug am EVU
	  "evua3": "5.0019", # Ampere Bezug am EVU
	  "lllp1": "1315",# Ladeleistung
	  "lllp2": "0",# Ladeleistung
	  "lllp3": "0",# Ladeleistung
	  "evuw": "-9",# Bezug/Überschuss am EVU
	  "pvw": "21",# PV Leistung
	  "evuv1": "231", #Volt am EVU
	  "evuv2": "232", #Volt am EVU
	  "evuv3": "229", #Volt am EVU
	  "ladestatusLP1": "1", # ob geladen wird aktuell
	  "ladestatusLP2": "1", # ob geladen wird aktuell
	  "ladestatusLP3": "0", # ob geladen wird aktuell
	  "zielladungaktiv": "0", #ob Zielladen aktiv
	  "lla1LP1": "6", #Ampere 
	  "lla2LP1": "0", #Ampere 
	  "lla3LP1": "0", #Ampere 
	  "lla1LP2": "10", #Ampere 
	  "lla2LP2": "0.000", #Ampere 
	  "lla3LP2": "0.000", #Ampere 
	  "llkwhLP1": "665.43", #Zäherstand am Ladepunktzähler
	  "llkwhLP2": "269.233", #Zäherstand am Ladepunktzähler
	  "llkwhLP3": "358.23", #Zäherstand am Ladepunktzähler
	  "evubezugWh": "1968573", #Zäherstand Bezug in Wh
	  "evueinspeisungWh": "10021315", #Zäherstand Einspeisung in Wh
	  "pvWh": "425299.8047", #Zählerstand PV in Wh
	  "speichersoc": "40.8",# SoC des Speichers in %
	  "socLP1": "66", # SoC des EV in %
	  "socLP2": "63", # SoC des EV in %
	  "speicherleistung": "-1302" #Lade / Entladeleistung des Speichers
	}

# Module erstellen

Ist ein Modul für den gewünscht Einsatszweck noch nicht verfügbar kann man dies selbst erstellen.
Wenn es läuft bitte reporten und ich füge es (einstellbar) dem Projekt hinzu.

Ein Modul ist immer ein Ordner mit dem Modulnamen im Ordner openWB/modules. Es besteht aus einem Shell script mit dem Namen main.sh. Sollten weitere Dateien benötigt werden liegen diese mit im Ordner. Bitte immer einen Timeout mit definieren um im Fehlerfall nicht hängen zu bleiben.

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


