# openWB




Die Software steht zur nicht kommerziellen Nutzung frei für jeden zur Verfügung.

	Unterstüztung ist gerne gesehen!
	Sei es in Form von Code oder durch Spenden
	Spenden bitte an info@snaptec.org

Kommerzielle Anfragen ebenso an info@snaptec.org
Weitere Infos unter http://openwb.de

# Haftungsausschluss
Es wird mit Kleinspannung aber auch 220V beim Anschluss der EVSE gearbeitet. 
Dies darf nur geschultes Personal. Die Anleitung ist ohne Gewähr und jegliches Handeln basiert auf eigene Gefahr.
Eine Fehlkonfiguration der Software kann höchstens ein nicht geladenes Auto bedeuten.
Falsch zusammengebaute Hardware kann lebensgefährlich sein. Im Zweifel diesen Part von einem Elektriker durchführen lassen.
Keine Gewährleistung für die Software - use at your own RISK!

# Wofür?
Steuerung einer EVSEwb für sofortiges laden, überwachung der Ladung, PV Überschussladung, Lastmanagement mehrerer WB und einiges mehr in Zukunft.


# Was wird benötigt?

Hardware:


- "EVSE WB" (! wichtig: Es wird die WB (WallBox)-Variante benötigt - nicht die "simple EVSE" !)
- Raspberry Pi 3 + Gehäuse (ev. gleich Hutschienengehäuse zur Installation in der WB)
- 0-5V DA-Konverter MCP4725 (0-5V zur Steuerung der Ladestromstärke an der EVSE) https://www.ebay.de/itm/Digital-Analog-Wandler-MCP4725-D-A-Wandler-12-Bit-Arduino-Raspberry-Pi/152972920605?hash=item239de5871d:g:DwkAAOSwW3VaxqNE
- Stromzähler mit Modbus zur Ladeleistungsmessung (z.B. SDM220/230 für 1-phasig, SDM630 für 3-phasig) https://www.ebay.de/itm/B-G-e-tech-LCD-Multifunktions-Dreh-Stromzahler-S0-RS485-10-100A-SDM630-Modbus/122226084121?hash=item1c753e0919:g:zToAAOSwcUBYKci1
- USB-RS485 Converter (z.B. https://www.ebay.de/itm/252784174363 )
- Bezugsstromzähler für +Bezug (positiv) bzw. -Überschuss (z.B. vorh. Smartmeter mit IR Lesekopf und VZLogger, separater SDM630v2,  -> weitere auf Anfrage)
- Auslesen der PV-Leistung (entsprechendes Softwaremodul fuer den Wechselrichter (Fronius derzeit unterstuetzt) oder separater SDM220/230 f. 1p bzw. SDM630 f. 3p)
- Schuetz entsprechend der max. Leistung
- Ladekabel mit CP-Steuerleitung (CP => Control Pilot)
- 2x PP- Abschlusswiderstände je Ladekabelende für max. Ladestromstärke des Ladekabels/Stecker/Buchse
- Typ1/2 Stecker

# Installation

Hardware:

MCP4725 an Raspberry verkabeln

	Vdd an +5V Pin 2

	GND an GnD Pin 6

	SCL an GPIO3 SCL Pin 5

	SDA an GPIO2 SDA Pin 3



MCP4725 an SimpleEVSE

	A0 an GND EVSE

	Vout an AN EVSE
Schaltbild EVSE mit SDM für die Ladeleistung und EVU / PV per Http Modulen (vzlogger, etc...)
![alt text](http://openwb.de/img/single_openWB_dac_wlan.jpg)

Alternativ wenn EVU und PV per SDM Zähler abgefragt werden soll:
![alt text](http://openwb.de/img/single_openWB_lanmb_wlan.jpg)


Für die Zusammenarbeit mit openWB müssen in der "EVSE WB" bestimmte Register gesetzt werden. Dies kann mit dem BT-Modul (HC-06) und der Android App (*.apk vorab installieren) realisiert werden:

APP-install: http://evracing.cz/evse/evse-wallbox/

Hinweise zur BT-Modulnutzung:

Um das BT-Modul nutzen zu können, muss sich die "EVSE WB" im "Modbus"-mode befinden. Dies ist häufig im Auslieferungszustand noch nicht der Fall.

Zur Aktivierung ist am besten ein Taster an AN + GND anzuschließen. Sofort wenn die "EVSE WB" mit 230V verbunden wird, ist innerhalb von 3s mind. 5x der Taster zu betätigen. Danach befindet sich die EVSE WB in einem temporären "Modbus"-mode.

Nun BT am Smartphone aktivieren und in den BT-Einstellungen das gefundene BT-Modul mit PW "1234" verbinden.

Danach die App starten und unter configure => launch settings die MAC-Adresse des BT-Moduls auswählen sowie die "Modbus slave address" = 1 setzen.

Nun in der App zurück gehen und mit "Connect" zum BT-Modul verbinden. Die LED des BT-Moduls muss von schnellem Dauerblinken auf sporadisches Blinken oder AUS umschalten (=> erfolgreicher Connect). Die APP-Anzeige springt auf "Disconnect".


notwendige Registereinstellungen für EVSE WB mit DAC-Modul (0-5V analog), um mit openWB zu arbeiten

("EVSE WB" mit Firmware 8, Bootloader 3, Stand 04.05.2018) 

Register 2001 = 1 (Modbus slave-ID) -> durch 5x Taster/3s bereits eingestellt

Register 2002 = 0 (erlaubt Ladestrom bis auf 0 = Ladungsstop), default=5 -> write value=0 -> "WRITE"

Register 2003 = 0 (Aktivierung AN-Eingang für 0-5V Analogsignalsteuerung) default=1 -> write value=0 -> "WRITE"

Register 2005 = 0 (Taster für Stromeinstellung sperren ) default=1 -> write value=0 -> "WRITE"

Der Rest kann bleiben.

Bereits mit 1x "WRITE" auf ein Register >=2000 wird Modbus dauerhaft aktiviert. Dies wäre hier schon mit Reg. 2002 geschehen.


SDM Einstellung:
	
	Baud 9600
	Stopbit 1
	Parität keine


Modbus Adapter anschließen:

A an A und B an B verkabeln. Es kann je nach Adapter erforderlich sein einen Abschlusswiderstand zu montieren.

150 Ohm haben sich als brauchbar erwiesen


Raspbian installieren

	https://www.raspberrypi.org/downloads/raspbian/



Den i2c Bus aktivieren.

Hierfür in der Konsole

        sudo raspi-config

ausführen.

	Punk 5 Interfacing Options auswählen

	P5 I2C auswählen und aktivieren.




In der Shell folgendes eingeben:

	curl -s https://raw.githubusercontent.com/snaptec/openWB/master/openwb-install.sh | sudo sh



Crontab anpassen:
	crontab -e
hier einfügen:

	* * * * /var/www/html/openWB/regel.sh >> /var/www/html/openWB/web/lade.log 2>&1 
	* * * * * sleep 10 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 20 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 30 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 40 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 
	* * * * * sleep 50 && /var/www/html/openWB/regel.sh >> /var/log/openWB.log 2>&1 


Für das Logging Feature:

Auf den Raspberry per ssh einloggen

	curl -s https://openwb.de/openwbm.sh | sudo sh

ausführen.
Zusätzlich crontab -e ausführen und

	@reboot sleep 10 && /usr/bin/curl http://localhost/metern/scripts/bootmn.php

mit eintragen. Hierdurch wird der Logging Daemon nach dem Reboot gestartet.

Das Logging ist erreichbar unter http://IPdesRPI/metern/

Zum Updaten:

	http://XXipXX/openWB/web/tools/update.php

aufrufen.

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


Der Raspberry funktioniert zuverlässig mit -gutes vorrausgesetzt- WLAN. Sprich er kann direkt mit EVSE WB und DAC in die Wallbox in der Garage.


 Nutzung von SMA Energy Metern:

Zunächst mit dem Raspberry per SSH verbinden.

Die Datei /var/www/html/openWB/web/files/smaemdconfig bearbeiten.
	
	vim /var/www/html/openWB/web/files/smaemdconfig

In Zeile 4 und Zeile 25 die Seriennummer(n) der Meter angeben. Bei mehreren Metern mit Leerzeichen trennen.

Nun das installscript ausführen:
	
	/var/www/html/openWB/web/tools/smaemd-install.sh

Anschließen im Webinterface in den Einstellungen die SMA Module auswählen und die Seriennummer entsprechend eintragen.



Taster am Raspberry zur Einstellung des Lademodi

Der Lademodi kann nicht nur über die Weboberfläche sondern auch an der Wallbox direkt eingestellt werden.
Hierzu müssen schließer Taster von GND (Pin 34) nach Gpio X  angeschlossen werden.

	SofortLaden GPIO 12, PIN 32

	Min+PV GPIO 16, PIN 36

	NurPV GPIO 6, Pin 31

	Aus Gpio 13, Pin 33
	

# Danke geht an:

	Frank für das Bereitstellen von Hardware und sein Modbus Wissen!
	Das Metern.org Projekt für die Loggingfunktionalität

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


# Module erstellen

Ist ein Modul für den gewünscht Einsatszweck noch nicht verfügbar kann man dies selbst erstellen.
Wenn es läuft bitte reporten und ich füge es (einstellbar) dem Projekt hinzu.

Ein Modul ist immer ein Ordner mit dem Modulnamen im Ordner openWB/modules. Es besteht aus einem Shell script mit dem Namen main.sh. Sollten weitere Dateien benötigt werden liegen diese mit im Ordner. Bitte immer einen Timeout mit definieren um im Fehlerfall nicht hängen zu bleiben.

Exemplarisch der Aufbau erklärt am bezug_http Modul:


	#!/bin/bash
	#Laden der openwb.conf Einstellung
	. /var/www/html/openWB/openwb.conf
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
	. /var/www/html/openWB/openwb.conf
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


