# openWB
Control your simpleEVSEwb with a Raspberry for various purposes

UPDATE:
derzeitige Version IST lauffähig und im Betastadium.
Wer das fertige stück software nachbauen und nutzen möchte muss sich noch ein wenig gedulden.
"Offizieller Release" nach Testphase.
Beta Tester sind herzlich willkommen.


Die Software steht zur nicht kommerziellen Nutzung frei für jeden zur Verfügung.
Spenden gerne an info@snaptec.org
Kommerzielle Anfragen ebenso an info@snaptec.org

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

Für 1-phasiges Laden:
- SimpleEVSEwb
- Raspberry pi 3
- 0-5V konverter MCP4725 (0-5V zur Steuerung der Ladestromstaerke an der EVSE)
- Stromzähler mit Modbus zur Ladeleistungsmessung (z.B. SDM220 / SDM230)
- USB-RS485 Converter (z.B. https://www.ebay.de/itm/252784174363 )
- Stromzähler zur Überschussmessung (z.b. SDM630v2, Zaehler mit IR Lesekopf und VZLogger usw <- wird beides unterstützt)
- Auslesen der PV (entsprechendes Modul fuer den Wechselrichter (Fronius derzeit unterstuetzt), oder z.B. SDM630)
- RPi Netzteil
- Schuetz entsprechend der max. Leistung
- Ladekabel mit Steuerleitung
- Typ1/2 Stecker

Für 1-phasiges Laden:
- SimpleEVSEwb
- Raspberry pi 3
- 0-5V konverter MCP4725 (0-5V zur Steuerung der Ladestromstaerke an der EVSE)
- Stromzähler mit Modbus zur Ladeleistungsmessung (z.B. SDM630v2)
- USB-RS485 Converter (z.B. https://www.ebay.de/itm/252784174363 )
- Stromzähler zur Überschussmessung (z.b. SDM630v2, Zaehler mit IR Lesekopf und VZLogger usw <- wird beides unterstützt)
- Auslesen der PV (entsprechendes Modul fuer den Wechselrichter (Fronius derzeit unterstuetzt), oder z.B. SDM220/SDM630 je nach Anzahl der Phasen)
- RPi Netzteil
- Schuetz entsprechend der max. Leistung
- Ladekabel mit Steuerleitung
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


Simple EVSE muss Register 2002 auf 0 stehen und Register 2003 auf 1. Dies kann per BT und der Android App gemacht werden.


Raspbian installieren

	https://www.raspberrypi.org/downloads/raspbian/



Den i2c Bus aktivieren.

In der Konsole

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


Zum Updaten:
!!BACKUP DER GEÄNDERTEN DATEIEN ERSTELLEN!!
Beim Update werden alle Dateien überschrieben.
Config muss neu angepasst werden.

	http://XXipXX/openWB/web/tools/update.php

aufrufen



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

